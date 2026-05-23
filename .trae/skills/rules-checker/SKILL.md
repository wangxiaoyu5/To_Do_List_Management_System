---
name: "rules-checker"
description: "Checks and updates project rules when business logic changes. Invoke when modifying database schema, adding new services, or changing business logic to ensure rules documentation stays synchronized."
---

# Rules Checker

This skill ensures that project rules documentation stays synchronized with code changes.

## When to Invoke

**CRITICAL: Invoke this skill when:**
1. Creating new database tables or modifying schema
2. Adding new service files
3. Changing business logic patterns
4. Introducing new coding patterns
5. Modifying API endpoints
6. Adding new middleware
7. Changing project structure

## Check Process

### Step 1: Analyze Changes
Identify what type of changes were made:
- Database schema changes?
- New service patterns?
- API changes?
- New file types?

### Step 2: Check Relevant Rules
Read the relevant rules files:
- `database-rules.md` - for DB changes
- `backend-rules.md` - for backend changes
- `frontend-rules.md` - for frontend changes
- `project-structure.md` - for structural changes

### Step 3: Identify Updates Needed
Check if changes require rule updates:
- New patterns not documented?
- Changed conventions?
- New best practices?
- Deprecated patterns?

### Step 4: Update Rules
If needed, update the relevant rules files to reflect:
- New patterns
- Updated examples
- Additional guidelines
- New checklists

## Rules Files Location

```
.trae/rules/
├── README.md                 # Rules index
├── project-rules.md          # General project rules
├── project-structure.md      # Directory structure
├── backend-rules.md          # Backend development
├── backend-workflow.md       # Backend workflow
├── database-rules.md         # Database development (Drizzle ORM)
├── frontend-rules.md         # Frontend development
└── frontend-design-tokens.md # UI/UX guidelines
```

## Checklist by Change Type

### Database Changes
- [ ] Schema follows naming conventions
- [ ] Required fields present (id, createdAt, updatedAt, isDeleted)
- [ ] Indexes properly defined
- [ ] Types exported correctly
- [ ] Service layer follows template
- [ ] Migration files generated
- [ ] `database-rules.md` updated if new patterns introduced

### Service Layer Changes
- [ ] Functions follow naming conventions
- [ ] Type safety maintained
- [ ] Error handling implemented
- [ ] Soft delete checks present
- [ ] Null value handling
- [ ] `backend-rules.md` updated if new patterns

### API Changes
- [ ] RESTful conventions followed
- [ ] Error responses consistent
- [ ] Request validation present
- [ ] Response types documented
- [ ] `backend-rules.md` updated

### Frontend Changes
- [ ] Components follow structure
- [ ] Design tokens used
- [ ] TypeScript types defined
- [ ] Error boundaries present
- [ ] `frontend-rules.md` updated

## Update Template

When updating rules, use this format:

```markdown
## [Section Name]

### [New/Updated Pattern]

Description of the pattern...

```typescript
// Example code
```

**When to use:** Description...

**Checklist:**
- [ ] Item 1
- [ ] Item 2
```

## Example Usage

**Scenario:** Adding a new database table

1. Create schema in `db/schema/index.ts`
2. Generate migration: `npm run db:generate`
3. Create service file following template
4. **Invoke this skill** to check if `database-rules.md` needs updates
5. If new pattern introduced, update rules
6. Run typecheck to verify

## Common Updates

### Adding New Table Pattern
Update `database-rules.md`:
- Add to "常用查询示例" section
- Update checklists if needed
- Add new service template if pattern differs

### New Service Pattern
Update `backend-rules.md`:
- Add to service layer section
- Update code examples
- Add new utility functions

### New API Pattern
Update `backend-rules.md`:
- Add to API design section
- Update request/response examples
- Add error handling patterns

## Verification

After updating rules:
1. Read the updated rules file
2. Verify examples are correct
3. Check formatting is consistent
4. Ensure all links work
5. Run typecheck to verify code examples

## Notes

- Rules should be **practical** and **actionable**
- Include **code examples** for all patterns
- Keep **checklists** up to date
- Document **why** not just **what**
- Update **version** and **date** when making changes
