package norootcontainers

has_run_as_non_root(c) if {
  c.securityContext.runAsNonRoot == true
}

has_non_root_user(c) if {
  c.securityContext.runAsUser > 0
}

violation contains msg if {
  input.review.kind.kind == "Pod"
  container := input.review.object.spec.containers[_]
  not has_run_as_non_root(container)
  not has_non_root_user(container)
  msg := sprintf("container %q must set runAsNonRoot or a non-zero runAsUser", [container.name])
}

violation contains msg if {
  input.review.kind.kind == "Pod"
  container := input.review.object.spec.initContainers[_]
  not has_run_as_non_root(container)
  not has_non_root_user(container)
  msg := sprintf("initContainer %q must set runAsNonRoot or a non-zero runAsUser", [container.name])
}
