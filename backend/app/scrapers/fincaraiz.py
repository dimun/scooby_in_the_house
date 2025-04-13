import re
import logging
import asyncio
import random
from typing import List, Dict, Any, Optional, AsyncGenerator
import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.schemas.property import PropertyCreate


logger = logging.getLogger(__name__)


class FincaRaizScraper:
    """
    Scraper for FincaRaiz.com.co website
    """

    BASE_URL = "https://www.fincaraiz.com.co"

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_property_listings(
        self,
        city: str,
        region: str,
        property_type: str = "casas-y-apartamentos",
        max_pages: int = 5,
    ) -> AsyncGenerator[List[PropertyCreate], None]:
        """
        Scrape properties from FincaRaiz based on city, region and property type.
        Yields each page's results for partial processing.

        Args:
            city: The city to search in
            region: The region/area within the city
            property_type: Type of properties to search for (e.g., "casas-y-apartamentos", "fincas", "casas-campestres", "cabanas")
                           Multiple types can be combined with "-y-" (e.g., "fincas-y-casas-campestres")
            max_pages: Maximum number of pages to scrape
        """
        url_template = (
            f"{self.BASE_URL}/venta/{property_type}/{city.lower()}/{region.lower()}"
        )

        for page in range(1, max_pages + 1):
            page_url = url_template
            if page > 1:
                page_url = f"{url_template}/pagina-{page}"

            logger.info(f"Scraping page {page}: {page_url}")

            try:
                async with self.session.get(page_url) as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch page {page}: {response.status}")
                        continue

                    html = await response.text()
                    soup = BeautifulSoup(html, "lxml")

                    # Find all property listings on the page
                    listings = self._extract_listings(soup, city, region)
                    if not listings:
                        logger.info(f"No more listings found on page {page}")
                        break

                    yield listings

                    # Add a random delay between 2-5 seconds between requests
                    delay = random.uniform(2, 5)
                    logger.debug(f"Waiting {delay:.2f} seconds before next request")
                    await asyncio.sleep(delay)

            except Exception as e:
                logger.error(f"Error scraping page {page}: {str(e)}")
                break

    @staticmethod
    def _extract_property_type(card: BeautifulSoup) -> Optional[str]:
        """Extract property type from card"""
        title_element = card.find("span", class_="lc-title")
        if not title_element:
            return None

        text = title_element.get_text(strip=True)
        if " en " in text:
            return text.split(" en ")[0]
        return None

    @staticmethod
    def _generate_title(property_type: Optional[str], city: str, surface: Optional[float], surface_unit: Optional[str]) -> str:
        """Generate title in format: {property_type} en {city} - {surface} {surface_unit}"""
        parts = []
        
        if property_type:
            parts.append(f"{property_type} en {city}")
        else:
            parts.append(f"{city}")
        
        if surface is not None and surface_unit:
            parts.append(f"{surface} {surface_unit}")
        
        return " - ".join(parts) if parts else ""

    def _extract_listings(
        self, soup: BeautifulSoup, city: str, region: str
    ) -> List[PropertyCreate]:
        """
        Extract property listings from a page
        """
        listings = []
        city = city[0].upper() + city[1:]
        region = region[0].upper() + region[1:]

        # Find all property cards with the listingCard class
        property_cards = soup.find_all("div", class_="listingCard")

        if not property_cards:
            logger.warning(
                "No property cards found. The website structure might have changed."
            )
            return []

        for card in property_cards:
            try:
                # Extract property URL
                url_tag = card.find("a", class_="lc-data")
                url = url_tag.get("href") if url_tag else None
                if url and not url.startswith("http"):
                    url = f"{self.BASE_URL}{url}"

                # Skip the base URL or empty URLs
                if not url or url == self.BASE_URL or url == f"{self.BASE_URL}/":
                    logger.warning(f"Skipping invalid URL: {url}")
                    continue

                # Extract image URLs using the new method
                image_urls = self._extract_image_urls(card)

                # Extract price
                price_text = card.find(text=re.compile(r"\$\s*[\d.,]+"))
                price = self._extract_price(price_text if price_text else "")

                # Extract rooms, bathrooms and surface from typology tag
                typology_tag = card.find("div", class_="lc-typologyTag")
                rooms = None
                bathrooms = None
                surface = None
                surface_unit = None

                if typology_tag:
                    typology_text = typology_tag.get_text(strip=True)
                    rooms = self._extract_rooms(typology_text)
                    bathrooms = self._extract_bathrooms(typology_text)
                    surface, surface_unit = self._extract_surface(typology_text)

                # Extract property type
                property_type = self._extract_property_type(card)

                # Generate title
                title = self._generate_title(property_type, city, surface, surface_unit)

                # Truncate title to fit the database column (max 256 chars)
                if title and len(title) > 256:
                    title = title[:252] + "..."

                listings.append(
                    PropertyCreate(
                        url=url,
                        price=price,
                        rooms=rooms,
                        bathrooms=bathrooms,
                        surface=surface,
                        surface_unit=surface_unit,
                        property_type=property_type,
                        title=title,
                        city=city,
                        region=region,
                        image_urls=image_urls,
                    )
                )

            except Exception as e:
                logger.error(f"Error extracting listing data: {str(e)}")
                continue

        return listings

    @staticmethod
    def _extract_price(price_text: str) -> Optional[float]:
        """Extract price value from text"""
        if not price_text:
            return None

        # Extract price values (handle formats like "$ 350.000.000")
        match = re.search(r"\$\s*([\d.,]+)", price_text)
        if match:
            # Remove dots (thousand separators in Spanish) but keep decimal points
            price_str = match.group(1).replace(".", "")
            try:
                return float(price_str)
            except (ValueError, TypeError):
                return None
        return None

    @staticmethod
    def _extract_number(text: str) -> Optional[int]:
        """Extract numeric value from text"""
        if not text:
            return None

        # Find all numbers in the text
        match = re.search(r"(\d+)", text)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, TypeError):
                return None
        return None

    @staticmethod
    def _extract_surface(text: str) -> tuple[Optional[float], Optional[str]]:
        """Extract surface area and unit from text"""
        if not text:
            return None, None

        # Find the numeric part and the unit
        match = re.search(r"(\d+)\s*m²", text)
        if match:
            try:
                value = float(match.group(1))
                return value, "m²"
            except (ValueError, TypeError):
                pass
        return None, None

    @staticmethod
    def _extract_rooms(text: str) -> Optional[int]:
        """Extract number of rooms from text"""
        if not text:
            return None

        match = re.search(r"(\d+)\s*Habs?", text)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, TypeError):
                pass
        return None

    @staticmethod
    def _extract_bathrooms(text: str) -> Optional[int]:
        """Extract number of bathrooms from text"""
        if not text:
            return None

        match = re.search(r"(\d+)\s*Baños", text)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, TypeError):
                pass
        return None

    def _extract_image_urls(self, card: BeautifulSoup) -> List[str]:
        """
        Extract image URLs from a property card by finding images with card-image-gallery--img class

        Args:
            card: BeautifulSoup object representing a property card

        Returns:
            List of image URLs
        """
        image_urls = []
        
        # Find all images with the specific class
        img_tags = card.find_all("img", class_="card-image-gallery--img")
        
        for img in img_tags:
            img_url = img.get("src")
            if img_url and not img_url.startswith("data:"):  # Skip data URLs
                if not img_url.startswith("http"):
                    img_url = f"{self.BASE_URL}{img_url}"
                image_urls.append(img_url)

        return image_urls
