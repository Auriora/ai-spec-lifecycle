# Feature Specification

## Summary

Fix stale search cache invalidation.

## Requirements

- **FR-001**: System MUST invalidate search cache when a document is deleted.

## Acceptance Criteria

1. Given a deleted document, when search is queried, then the deleted document
   does not appear.
