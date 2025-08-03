package denyservicewithoutowner

violation contains msg if {
  input.review.kind.kind == "Service"
  not input.review.object.metadata.labels.owner
  msg := sprintf("Service %q is missing required 'owner' label", [input.review.object.metadata.name])
}
