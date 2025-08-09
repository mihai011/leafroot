"""Module for testing particles controller."""

from fastapi import status

from tests import DataSource


async def test_particles(async_session):
    """Testing particles."""

    ds = DataSource(async_session)
    await ds.make_user()
    # make proton
    payload_particle = {"charge": 123.23}
    payload_atom = {"x": 1, "y": 1, "z": 1}

    response = await ds.client.post(
        "/atoms/create_atom",
        headers=ds.headers["Test_user"],
        json=payload_atom,
    )
    assert response.status_code == status.HTTP_200_OK
    atom_id = response.json()["item"]["id"]
    payload_particle["atom_id"] = atom_id

    response = await ds.client.post(
        "/atoms/proton", headers=ds.headers["Test_user"], json=payload_particle
    )
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.get(
        "/atoms/proton",
        params=payload_particle,
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.post(
        "/atoms/neutron",
        headers=ds.headers["Test_user"],
        json=payload_particle,
    )
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.get(
        "/atoms/neutron",
        params=payload_particle,
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.post(
        "/atoms/electron",
        headers=ds.headers["Test_user"],
        json=payload_particle,
    )
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.get(
        "/atoms/electron",
        params=payload_particle,
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK
