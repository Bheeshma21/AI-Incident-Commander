from unittest.mock import MagicMock, patch

from backend.llm import ask_llm


def test_ask_llm():
    """Test ask_llm without making a real Groq API request."""

    mock_response = MagicMock()

    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content=(
                    "An HTTP 500 error means the server "
                    "encountered an unexpected condition."
                )
            )
        )
    ]

    with patch("backend.llm.get_client") as mock_get_client:

        mock_client = MagicMock()

        mock_client.chat.completions.create.return_value = (
            mock_response
        )

        mock_get_client.return_value = mock_client

        response = ask_llm(
            system_prompt=(
                "You are a helpful AI engineering assistant."
            ),
            user_prompt=(
                "Explain what an HTTP 500 error means "
                "in one sentence."
            ),
        )

        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0

        mock_client.chat.completions.create.assert_called_once()