# Three teams, three Customers

The fictional company Northstar had a familiar migration problem. Sales called
every paying account a Customer. Support called the person who opened a ticket
a Customer. Finance called a legal entity a Customer. A dashboard joined the
three tables on a display name and quietly counted subsidiaries twice.

The ontology workshop did not begin with a class diagram. It began with the
decision: “Which accounts should receive the new service tier?” The team wrote
three competency questions, listed exclusions, and assigned an owner to the
definition. `Customer` became a scoped term; `Person`, `Organization`, and
`Account` remained separate classes. Source identifiers stayed attached to each
mapping decision.

Try the same shape in the [business pack](../../examples/business-projects/README.md)
and the [one-word visual](../../media/exports/infographic-one-word-three-meanings.svg).
The pack models service ownership; customer identity reconciliation and its
review queue remain workshop exercises. The pack is synthetic, so a passing query demonstrates repeatability, not a
real account decision.

The first pilot measured false merges and review time, not revenue. When two
records still had the same legal name, the resolver abstained and put them in a
queue. That small refusal was more valuable than an apparently complete table:
the team could see exactly where a human needed to decide.
