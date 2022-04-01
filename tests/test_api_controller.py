"""
Module for testing api controller
"""
import pytest
from aioresponses import aioresponses


from tests import DataSource
from tests.conftest import temp_db


@pytest.mark.asyncio
@temp_db
async def test_api(session):
    """
    test api request controller
    """

    ds = DataSource(session)
    await ds.make_user()

    

    payload_api = {
        "url": "http://fake_url.com",
        "body": {},
        "method": "GET",
        "params":{},
        "headers": {},
    }
    with aioresponses() as mocked:
        mocked.get(payload_api['url'], status=200, body="test1")
        response = await ds.client.post(
            "/api/external", json=payload_api, headers=ds.headers["Test_user"]
        )
    assert response.status_code == 200
    assert response.json() == {'message': 'api called', 'item': "test1", 'status': 200}

    
    key_and_missing = {
        "url" : "Url",
        "body" : "Body",
        "method": "Method",
        "params": "Params",
        "headers": "Headers"
    }

    for key in key_and_missing.keys():

        value = payload_api.pop(key)

        response = await ds.client.post(
                "/api/external", json=payload_api, headers=ds.headers["Test_user"]
            )
        assert response.status_code == 200
        assert response.json() == {'message': '{} not found in payload!'.format(key_and_missing[key]), 
        'item': None, 'status': 400}

        payload_api[key] = value
