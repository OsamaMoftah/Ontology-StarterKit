# The evidence room at Northstar

During a fictional diligence project, a client asked whether a portfolio asset
was ready for a regulatory discussion. One slide cited a dated publication; a
second source used a different indication name; an internal note had no source
span. A language model produced a confident paragraph that blended all three.

The consulting team modelled `Claim`, `Evidence`, `Source`, `Asset`, and
`Indication` separately. Every claim received a status: supported, contested, or
unknown. The answer template required a source path and data version. The
unsupported claim did not disappear; it became a reviewer task with a next
action and owner.

Run the [consulting evidence-room pack](../../examples/consulting-evidence-room/README.md)
and inspect the [evidence-room visual](../../media/exports/consulting-evidence-room.svg).
The records are invented and deliberately small. They show a workflow contract,
not clinical, regulatory, or investment advice.

The client still needed a medical and regulatory review. The ontology made that
handoff explicit instead of making a generated answer look like approval.
