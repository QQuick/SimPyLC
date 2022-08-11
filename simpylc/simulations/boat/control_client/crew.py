'''
====== Requirements

The control, symbolized by a "virtual" crew, steers the boat along a sequence of approximately straight line segments.
Since we're dealing with a sailing vessel, it's not always possible to directly follow a given line segment.
If needed the vessel will ply against the wind to get to the end of the line segment.

====== Testspecification

====== Design

The crew consists of the following hierarchy:

--- Captain

- Plans the overal route depending on e.g. prevalent wind directions.
- Breaks this route down into segments short enough te be assumed straight line segments rather than loxodromes, each between two 'waypoints'.
- The list of waypoints is communicated to the Helmsman.
- Climate change is assumed to go slow enough to postpone or forego any clever tricks at the poles.

--- Helmsman

- Steer the boat along a sequence of segments as defined above.
- Each segment ends with rounding a waypoint.
- If the next waypoint is exactly ahead, the current one is rounded at the side the next one should be rounded.
- If a waypoint is in the dead sector, a cross gauge is done on the waypoint, followed by tacking.
- Gibing happens whenever needed by shortening and subsequent lengthening of the sheet and has no influence on the course.
- The boat hardware may (initially ;) ) not support sheet control, in which case the sheet length output is simply ignored.

--- Deckhand

- Deals directly with the boat hardware.
- Provides low level safety interlocks to prevent hardware damage.
- Abstracts away hardware peculiarities, thus enabling easy exchange and second sourcing of hardware parts.
- Converts between general engineering conventions and hardware c.q. application dependent conventions.

Any crew member can directly contact any other crew member.
Any crew member can make use of the Almanac, that embodies basic nautical and geometric knowledge.

'''

import sys as ss

import captain as ct
import helmsman as hm
import deckhand_twin as dh

this = ss.modules [__name__]

deckhand = dh.Deckhand (this)
helmsman = hm.Helmsman (this)
captain = ct.Captain (this)

deckhand.sweep = helmsman.sweep
captain.navigate ()

