---
inclusion: auto
---

# GitLab Code Review Guidelines

## Khi Review Merge Request

### 1. Phân tích MR Overview
- Đọc title và description
- Kiểm tra số files thay đổi
- Xem liên quan đến feature nào

### 2. Review Code Changes
```
Xem MR #123 và phân tích các thay đổi
```

Cần chú ý:
- **Code quality**: Clean code, naming conventions
- **Business logic**: Đúng requirements không?
- **Performance**: Có query N+1, memory leak?
- **Security**: SQL injection, XSS, authentication issues
- **Error handling**: Try-catch, validation đầy đủ
- **Tests**: Có unit tests không? Coverage đủ không?

### 3. Check Database Impact
Nếu MR có thay đổi database:
```
Describe table Users và xem có conflict với changes không
```

### 4. Verify with Requirements
Nếu có document liên quan:
```
Đọc file feature-spec.pdf và verify MR có implement đầy đủ không
```

### 5. Check Pipeline Status
```
Xem pipelines của MR này có pass không
```

## Review Checklist

### Code Structure
- [ ] Code dễ đọc và maintain
- [ ] Proper separation of concerns
- [ ] Reusable components
- [ ] No duplicate code

### Functionality
- [ ] Implement đúng requirements
- [ ] Edge cases được handle
- [ ] Error messages clear và helpful

### Performance
- [ ] No unnecessary database calls
- [ ] Efficient algorithms
- [ ] Proper caching nếu cần

### Security
- [ ] Input validation
- [ ] No sensitive data exposed
- [ ] Proper authentication/authorization
- [ ] SQL injection prevention

### Testing
- [ ] Unit tests cover main scenarios
- [ ] Integration tests nếu cần
- [ ] Test cases include edge cases

### Documentation
- [ ] Code comments cho logic phức tạp
- [ ] API documentation updated
- [ ] README updated nếu cần

## Common Issues to Look For

### Angular Specific
- Memory leaks (unsubscribe Observables)
- Change detection issues
- Improper use of async pipe
- Component lifecycle hooks misuse

### SQL Server
- Missing indexes
- N+1 query problems
- Transaction handling
- Proper use of stored procedures

### General
- Hardcoded values nên dùng config
- Magic numbers nên define constants
- Console.logs nên remove trước production
- TODO comments nên resolve

## Example Review Comments

### Good Comment:
```
Suggestion: Consider using a stored procedure here for better performance
and to centralize business logic. Current implementation makes 3 separate
queries that could be combined.
```

### Bad Comment:
```
This is wrong.
```

## Auto-Review Workflow

Khi có MR mới, Kiro có thể:
1. List recent MRs
2. Pick MR cần review
3. Get MR details và changes
4. Analyze code với context từ database schema
5. Check requirements document nếu có
6. Generate review comments
7. Suggest improvements

## Integration với Hooks

Có thể setup hook để auto-review:
- On `userTriggered`: Review MR được select
- Schedule: Review tất cả open MRs mỗi ngày

Example hook command:
```bash
# Review MR #123
kiro "Review MR #123 thoroughly and provide feedback"
```
