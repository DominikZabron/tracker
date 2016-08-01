#!/usr/bin/env python
from __future__ import absolute_import

from tracker.models import Base
from tracker.db import engine
# from tests.test_utils import engine


if __name__ == '__main__':
    Base.metadata.create_all(engine)
