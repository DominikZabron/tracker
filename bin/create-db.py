#!/usr/bin/env python
from __future__ import absolute_import

from tracker.models import Base
from tracker.db import engine


if __name__ == '__main__':
    Base.metadata.create_all(engine)
