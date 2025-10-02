# Database Collections & Models

## `products`
- `internalId`: String (primary key, composed of `productId_subTypeName`).
- `productId`: Integer (TCGCSV identifier).
- `groupId`, `categoryId`: Integers for grouping and category taxonomy.
- `name`, `number`, `rarity`, `subTypeName`: Strings describing the card.
- `imageUrl`, `tcgplayerUrl`: External references.
- `marketPrice`, `lowPrice`, `midPrice`, `highPrice`, `directLowPrice`: Pricing metrics.
- `createdAt`, `updatedAt`: Timestamps for import tracking.

## `buylist_entries`
- `internalId`: String (references `products.internalId`).
- `priceMultiplier`: Decimal; multiplier applied to a reference price.
- `priceOverride`: Decimal; optional fixed payout.
- `maxQuantity`: Integer limit per store-defined timeframe.
- `disabled`: Boolean indicating customer visibility.
- `notes`: Optional text for internal instructions.
- `createdBy`, `updatedBy`: User references (username or user ID).
- `createdAt`, `updatedAt`: Timestamps.

## `buylist_progress`
- `internalId`: String (references `products.internalId`).
- `maxQuantity`: Integer; system-enforced limit.
- `pendingQuantity`: Integer; carts submitted but not processed.
- `boughtQuantity`: Integer; total accepted/processed quantity.
- `autoDisabledAt`: Timestamp when the item was auto-disabled.
- `updatedAt`: Timestamp of last recalculation.

## `buy_carts`
- `cartId`: ObjectId.
- `status`: Enum (`draft`, `submitted`, `accepted`, `processed`, `reviewed`, `finalized`, `completed`, `cancelled`).
- `username`: String (customer reference) or `null` for guest carts.
- `dropOffType`: Enum (`in_store`, `shipping`).
- `items`: Array of subdocuments with `internalId`, `requestedCondition`, `requestedQuantity`, `verifiedCondition`, `verifiedQuantity`, `payoutEach`, `notes`.
- `payout`: Subdocument with `cash`, `credit`, `creditBonus`.
- `history`: Array of status changes with timestamps, actor, and notes.
- `attachments`: Array of file metadata references.
- `employeeName`, `processedBy`: Strings referencing employees.
- `createdAt`, `submittedAt`, `processedAt`, `reviewedAt`, `finalizedAt`, `completedAt`, `cancelledAt`.
- `managerCorrections`: Array of corrections applied during review.

## `users`
- `userId`: ObjectId.
- `username`: Unique string.
- `passwordHash`: Hashed password.
- `role`: Enum (`customer`, `employee`, `manager`, `admin`).
- `contact`: Subdocument with email, phone, and notification preferences.
- `status`: Enum (`active`, `inactive`, `locked`).
- `createdAt`, `updatedAt`, `lastLoginAt`.

## `server_settings`
- `storeName`: String.
- `creditBoostPercentage`: Decimal.
- `conditionPercentages`: Map of condition to payout percentage.
- `enabledCategories`: Array of category IDs.
- `allowUserAccounts`, `allowInStoreDropOff`, `allowShippedDropOff`: Booleans.
- `announcementBanner`: Optional string.
- `updatedBy`: User reference.
- `updatedAt`: Timestamp.

## `audit_logs`
- `logId`: ObjectId.
- `action`: String identifier.
- `collectionName`: String.
- `documentId`: Reference to affected document.
- `performedBy`: User reference.
- `timestamp`: Timestamp.
- `details`: JSON object capturing before/after deltas.
- `ipAddress`, `userAgent`: Optional metadata.

## `emergency_disables`
- `ruleId`: ObjectId.
- `type`: Enum (`group`, `category`, `product`).
- `targetId`: Identifier for the disabled entity.
- `reason`: Text.
- `disabledBy`: User reference.
- `disabledAt`: Timestamp.
- `expiresAt`: Optional timestamp for auto re-enable.

## `inventory_imports`
- `importId`: ObjectId.
- `status`: Enum (`draft`, `generated`, `exported`, `synced`).
- `cartIds`: Array of `buy_carts.cartId`.
- `totals`: Array of per-product aggregates (internalId, quantity, payout, condition mix).
- `summary`: Totals for cash, credit, cards count.
- `exportMetadata`: Subdocument (format, file references, generatedAt, generatedBy).
- `notes`: Text.
- `createdAt`, `updatedAt`.

## `import_runs`
- `runId`: ObjectId.
- `type`: Enum (`tcgcsv`).
- `status`: Enum (`pending`, `running`, `succeeded`, `failed`).
- `startedAt`, `completedAt`.
- `stats`: JSON object with counts (inserted, updated, skipped).
- `error`: Optional error message/stack trace.

## `analytics_cache`
- `cacheId`: ObjectId.
- `metric`: String identifier (e.g., `spend_summary-weekly`).
- `parameters`: JSON object describing filters.
- `data`: Aggregated results snapshot.
- `generatedAt`: Timestamp.
- `expiresAt`: Timestamp for cache invalidation.
