
from contextlib import nullcontext as does_not_raise

import aiohttp
import pytest
import pytest_asyncio

from infrastructure.exceptions import RequestError
from services.data_processors import get_page_content, parse_page_content


@pytest_asyncio.fixture
async def html_content():
    url = "https://4ege.ru/novosti-ege/4023-shkala-perevoda-ballov-ege.html"
    return await get_page_content(url)


@pytest.mark.parametrize(
    ["url", "expectation"],
    [
        ("https://4ege.ru/novosti-ege/4023-shkala-perevoda-ballov-ege.html", does_not_raise()),
        ("https://google.com", does_not_raise()),
        ("https://mos.ru", does_not_raise()),

        ("https://httpbin.org/status/201", pytest.raises(RequestError)),
        ("https://httpbin.org/status/204", pytest.raises(RequestError)),
        ("https://httpbin.org/status/300", pytest.raises(RequestError)),
        ("https://httpbin.org/status/304", pytest.raises(RequestError)),
        ("https://httpbin.org/status/403", pytest.raises(RequestError)),
        ("https://httpbin.org/status/429", pytest.raises(RequestError)),
        ("https://httpbin.org/status/500", pytest.raises(RequestError)),
        ("https://httpbin.org/status/502", pytest.raises(RequestError)),

        ("https://abchjrie.com", pytest.raises(aiohttp.client_exceptions.ClientConnectorDNSError)),
        ("https://hfrhufr.org", pytest.raises(aiohttp.client_exceptions.ClientConnectorDNSError)),
        ("https://frefer.ru", pytest.raises(aiohttp.client_exceptions.ClientConnectorDNSError)),
    ]
)
@pytest.mark.asyncio
async def test_get_page_content(url, expectation):
    with expectation:
        result = await get_page_content(url)

        assert isinstance(result, str)
        assert result.lower().startswith('<html>') or result.lower().startswith('<!doctype html>')


def test_parse_page_content(html_content):
    result = parse_page_content(html_content)

    assert isinstance(result, list)
    assert len(result) > 0
    
    assert all(hasattr(item, 'title') for item in result)
    assert all(hasattr(item, 'marks') for item in result)
