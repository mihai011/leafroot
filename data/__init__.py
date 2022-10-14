"""module for related data."""

from data.models.user import User, Base
from data.models.atom import Atom, Electron, Neutron, Proton

from data.models import get_session, async_session
