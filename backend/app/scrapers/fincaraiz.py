import re
import logging
import asyncio
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
                        break

                    html = await response.text()
                    soup = BeautifulSoup(html, "lxml")

                    # Find all property listings on the page
                    listings = self._extract_listings(soup, city, region)
                    if not listings:
                        logger.info(f"No more listings found on page {page}")
                        break

                    yield listings

                    # Add a small delay between requests
                    await asyncio.sleep(2)

            except Exception as e:
                logger.error(f"Error scraping page {page}: {str(e)}")
                break

    def _extract_listings(
        self, soup: BeautifulSoup, city: str, region: str
    ) -> List[PropertyCreate]:
        """
        Extract property listings from a page
        """
        listings = []

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

                # Extract rooms
                rooms_text = card.find(text=re.compile(r"(\d+)\s*Habs", re.IGNORECASE))
                rooms = self._extract_number(rooms_text if rooms_text else "")

                # Extract bathrooms
                bathrooms_text = card.find(
                    text=re.compile(r"(\d+)\s*Baños", re.IGNORECASE)
                )
                bathrooms = self._extract_number(
                    bathrooms_text if bathrooms_text else ""
                )

                # Extract surface
                surface_text = card.find(
                    text=re.compile(r"(\d+[\.,]?\d*)\s*m²", re.IGNORECASE)
                )
                surface, surface_unit = self._extract_surface(
                    surface_text if surface_text else ""
                )

                # Extract property type and title
                title_elements = card.find_all(
                    lambda tag: tag.name == "div" and tag.get_text(strip=True)
                )
                property_type = None
                title = None

                for element in title_elements:
                    text = element.get_text(strip=True)
                    if "en Venta" in text or "en venta" in text:
                        property_type = (
                            text.split(" en ")[0] if " en " in text else None
                        )
                        title = text
                        break

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
        match = re.search(r"([\d.,]+)\s*([a-zA-Z²]+)", text)
        if match:
            try:
                # Replace comma with dot for decimal point
                value = float(match.group(1).replace(",", "."))
                unit = match.group(2)
                return value, unit
            except (ValueError, TypeError):
                pass
        return None, None

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
