import time
from typing import Any, Optional

class JsonParser:
    def __init__(self, raw, og_url):
        self.raw = raw
        self.og_url = og_url

    def parse(self):
        return {
            "timestamp": int(time.time()),
            "RPC": self._get_rpc(),
            "url": self.og_url,
            "title": self._get_title(),
            "marketing_tags": self._get_marketing_tags(),
            "brand": self._get_brand(),
            "section": self._get_section(),
            "price_data": self._get_price_data(),
            "stock": self._get_stock(),
            "assets": self._get_assets(),
            "metadata": self._get_metadata(),
            "variants": 1
        }
    
    def _get_rpc(self) -> str:
        return self.raw.get("uuid")
    
    def _get_title(self) -> str:
        title = self.raw.get("name")
        color = None
        volume = None

        for block in self.raw.get("description_blocks"):
            code = block.get("code")
            if code == "cvet":
                color = block.get("values")[0].get("name")
            elif code == "obem":
                volume = f"{block.get("min")}{block.get("unit")}"

        parts = [title]
        if color:
            parts.append(color)
        if volume:
            parts.append( volume)

        return ", ".join(filter(None, parts))
    
    def _get_marketing_tags(self) -> list[str]:
        return [lables.get("title") for lables in self.raw.get("filter_labels")]
    
    def _get_brand(self) -> str | None:
        for block in self.raw.get("description_blocks"):
            if block.get("code") == "brend":
                return block.get("values")[0].get("name")
        return None
    
    def _get_section(self) -> list[str]:
        category = self.raw.get("category")
        parent = category.get("parent")
        if parent:
            return [parent.get("name")]
        return []

    def _get_price_data(self) -> dict[str, Any]:
        current = self.raw.get("price")
        original = self.raw.get("prev_price")

        return {
            "current": float(current),
            "original": float(original) if original else float(current),
            "sale_tag": self._get_sale_tag(original, current)
        }

    def _get_sale_tag(self, original: Optional[float], current: Optional[float]) -> Optional[str]:
        if original is not None:
            return f"Скидка {int((original - current) * 100 / original)}%"
        return None

    def _get_stock(self) -> dict[str, Any]:
        count = self.raw.get("quantity_total")
        return {
            "in_stock": True if count > 0 else False,
            "count": count
        }
    
    def _get_assets(self) -> dict[str, list[str]]:
        return {
            "main_image": self.raw.get("image_url"),
            "set_images": [],
            "view360": [],
            "video": []
        }

    def _get_metadata(self) -> dict[str, str]:
        data = {}
        for block in self.raw.get("description_blocks"):
            values = block.get("values")
            title = block.get("title")
            unit = block.get("unit")
            if values:
                value = values[0].get("name")
            else:
                value = block.get("min")
            data[title] = f"{value}{unit}"
        data["Артикул"] = str(self.raw.get("vendor_code"))
        data["Код товара"] = self.raw.get("uuid")
        return {"__description": self._get_description(), **data}

    def _get_description(self) -> str | None:
        if len(self.raw.get("text_blocks")) > 0:
            return self.raw.get("text_blocks")[0].get("content")
        return None




