# Metric identities

Write the identity **before** root-cause analysis. If you cannot write it, you do not yet understand the metric.

```text
Revenue = Active customers × Orders/customer × AOV
DAU     = New + Retained + Resurrected
CR      = Successful conversions / Eligible population
```

For a ratio, write both a **count identity** and a **rate identity**: the count is `numerator events` and `denominator population`, and the rate is their quotient. A move in the rate can come from the numerator, the denominator, or the mix between them — decompose all three.

## Checklist

- Numerator and denominator at the same grain and the same eligible set?
- Rate vs count — a mix shift can look like a rate change (weighted average)
- Leading vs lagging (signup != activation != revenue)
- Cohort-dependent metrics are not "users this week"
- Conversion metrics need a time window applied to the same entity
- Identity resolution: are anonymous and known users merged the same way in both periods?

## Ratio vs derived

- Ratio: two metrics, one entity, declared filters only on dimensions that exist
- Derived: `profit = revenue - cost`, or a growth rate against a **named** baseline
