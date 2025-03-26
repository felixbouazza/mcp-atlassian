"""Module for Confluence page operations."""

import logging

import io
import base64

from ..models.confluence import ConfluenceAttachment
from .client import ConfluenceClient

logger = logging.getLogger("mcp-atlassian")


class AttachmentsMixin(ConfluenceClient):
    """Mixin for Confluence attachment operations."""

    def get_attachments_from_page_id(
        self, page_id: str
    ) -> list[ConfluenceAttachment]:
        """
        Get attachments from a specific page.

        Args:
            page_id: The ID of the page to retrieve

        Returns:
            List of ConfluenceAttachment models containing the attachments and metadata
        """
        attachments = self.confluence.get_attachments_from_content(page_id=page_id)["results"]
        attachment_models = []
        for attachment in attachments:
            filename = attachment["title"] 
            if not ".png" in filename and not ".jpg" in filename and not ".jpeg" in filename:
                continue
            response = self.confluence.get(str(attachment["_links"]["download"]), not_json_response=True)
            image_base64 = base64.b64encode(response).decode("utf-8")
            attachment_models.append(image_base64)
    
        return attachment_models