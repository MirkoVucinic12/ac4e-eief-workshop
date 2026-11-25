# Undocumented sample restriction (planted)

A draft analysis note drops all Pennsylvania stores "because they look noisy"
and still reports the New Jersey before-and-after change as a difference-in-differences estimate.

Why this fails:

- The documented sample covers NJ and PA stores observed in both waves.
- The provenance log must record any sample restriction before results are reported.
- Difference-in-differences compares two groups over time; a single-state change estimates a different quantity.
