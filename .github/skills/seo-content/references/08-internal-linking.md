# Internal Linking Optimization Guide

## 목표

사이트 아키텍처를 개선하고, authority 를 분산시키며, orphan pages 를 해결한다. Internal linking 은 개별 페이지 최적화 (on-page SEO) 와 성격이 다르며, 사이트 전체의 crawlability 와 ranking distribution 에 영향을 미친다.

---

## 1. Link Structure Analysis

### Link Distribution 테이블

| Links per Page | Page Count | Percentage |
|----------------|------------|------------|
| 0 (Orphan) | [X] | [X]% |
| 1-5 | [X] | [X]% |
| 6-10 | [X] | [X]% |
| 11-20 | [X] | [X]% |
| 20+ | [X] | [X]% |

### Top Linked Pages

| Page | Internal Links | Authority | Notes |
|------|----------------|-----------|-------|
| [URL 1] | [X] | High | [notes] |
| [URL 2] | [X] | High | [notes] |
| [URL 3] | [X] | Medium | [notes] |

### Under-Linked Important Pages

| Page | Current Links | Traffic | Recommended Links |
|------|---------------|---------|-------------------|
| [URL 1] | [X] | [X]/mo | [X]+ |
| [URL 2] | [X] | [X]/mo | [X]+ |

**Structure Score**: [X]/10

### 빠른 판단 기준

- Orphan pages가 5% 이상이면 즉시 해결이 필요하다
- Important pages가 3 clicks 이내에 접근 가능해야 한다
- High-traffic pages가 commercial pages로 링크해야 한다
- Links per page가 5-15 개 범위가 optimal이다
- Structure Score가 7/10 미만이면 재구성이 필요하다

---

## 2. Orphan Page Detection

Orphan pages 은 내부 링크가 전혀 없어 사용자와 검색 엔진이 발견하기 어려운 페이지다.

### Orphan Pages Found: [X]

| Page | Traffic | Priority | Recommended Action |
|------|---------|----------|-------------------|
| [URL 1] | [X]/mo | High | Link from [pages] |
| [URL 2] | [X]/mo | Medium | Add to navigation |
| [URL 3] | 0 | Low | Consider deleting/redirecting |

### Fix Strategy

**High Priority Orphans** (have traffic/rankings):
1. [URL] - Add links from: [relevant pages]
2. [URL] - Add links from: [relevant pages]

**Medium Priority Orphans** (important but low traffic):
- Add to relevant category pages
- Include in navigation or footer
- Link from related blog posts

**Low Priority Orphans** (no traffic, low value):
- Consider 301 redirect to relevant page
- Delete if truly obsolete

### 빠른 판단 기준

- Orphan pages with traffic은 High Priority로 즉시 해결한다
- No traffic, low value pages는 redirect 또는 delete를 고려한다
- Orphan pages는 search console에서도 발견이 어렵다
- High Priority Orphans는 최소 3 개 이상의 internal links를 추가한다
- Orphan page count를 monthly로 tracking한다

---

## 3. Authority Flow Mapping

PageRank flow 를 시각화하여 authority 가 어떻게 분산되는지 분석한다.

### Authority Flow Principles

1. **Homepage authority is highest** — homepage 에서 가까운 페이지일수록 authority 를 더 받는다
2. **Links pass equity** — 각 internal link는 source page 의 authority 를 destination 에 전달한다
3. **Too many links dilute value** — 한 페이지에 링크가 너무 많으면 각각이 받는 equity 가 줄어든다
4. **Orphan pages get no equity** — 내부 링크가 없으면 authority 전달이 안 된다

### Authority Distribution Checklist

- [ ] Homepage links to key commercial pages directly
- [ ] Important pages are within 3 clicks from homepage
- [ ] High-traffic pages link to conversion-target pages
- [ ] Cluster content interlinks within topic groups
- [ ] No important page is more than 5 clicks from homepage

### 빠른 판단 기준

- Homepage authority가 가장 높고, 가까운 페이지가 더 많은 equity를 받다
- Links가 너무 많으면 각 link의 equity가 dilute된다
- Orphan pages는 authority 전달이 전혀 안 된다
- Homepage에서 commercial pages로 직접 링크를 추가한다
- Important pages는 3 clicks 이내에 위치해야 한다

---

## 4. Topic Cluster Linking

Pillar-cluster 모델을 사용하여 주제별 authority 를 강화한다.

### Pillar-Cluster Structure

```
Pillar Page (broad topic)
├── Cluster Content 1 (subtopic)
├── Cluster Content 2 (subtopic)
├── Cluster Content 3 (subtopic)
└── Cluster Content 4 (subtopic)
```

### Linking Rules

1. **Pillar → All Clusters**: Pillar page 는 모든 cluster content 에 링크한다
2. **All Clusters → Pillar**: 모든 cluster content 는 pillar page 에 링크한다
3. **Cluster ↔ Cluster**: Related cluster content 간에 cross-link 한다
4. **No orphan clusters**: 모든 cluster 는 pillar 와 연결되어야 한다

### Example: SEO Topic Cluster

**Pillar**: "Complete Guide to SEO"
**Clusters**:
- "Keyword Research Basics"
- "On-Page SEO Checklist"
- "Technical SEO Audit"
- "Link Building Strategies"

**Linking Pattern**:
- Pillar links to all 4 clusters
- All 4 clusters link back to pillar
- "Keyword Research" links to "On-Page SEO" (related topics)
- "Technical SEO" links to "On-Page SEO" (overlapping concepts)

### 빠른 판단 기준

- Pillar page는 모든 cluster content에 링크해야 한다
- 모든 cluster content는 pillar page에 링크해야 한다
- Related cluster content 간에 cross-link를 추가한다
- Orphan clusters는 pillar와 연결이 필수다
- Topic cluster는 주제별 authority를 강화한다

---

## 5. Anchor Text Optimization

Anchor text 는 링크의 destination 을 설명해야 한다.

### Anchor Text Best Practices

| Do | Don't |
|----|-------|
| "Learn more about keyword research" | "Click here" |
| "Our SEO pricing plans" | "This page" |
| "Read the complete guide" | "Here" |
| "See our case studies" | "Link" |

### Anchor Text Distribution

- **Exact match** (primary keyword): 10-20%
- **Partial match** (keyword variations): 30-40%
- **Branded** (brand name): 20-30%
- **Generic** (learn more, read more): 10-20%
- **Naked URLs**: <5%

### Anchor Text Checklist

- [ ] "Click here" and "read more" are minimized
- [ ] Anchor text describes destination content
- [ ] Primary keyword appears naturally in some anchors
- [ ] No keyword stuffing in anchor text
- [ ] Mix of exact, partial, branded, and generic anchors

### 빠른 판단 기준

- "Click here"와 "read more"는 최소화해야 한다
- Anchor text는 destination content를 설명해야 한다
- Primary keyword는 자연스럽게 일부 anchors에 포함한다
- Keyword stuffing은 금지다
- Exact, partial, branded, generic의 mix를 유지한다

---

## 6. Implementation Priorities

### P0 (Immediate)

1. Fix orphan pages with existing traffic
2. Add internal links to high-value conversion pages
3. Remove broken internal links

### P1 (This Week)

1. Build pillar-cluster linking structure for main topics
2. Add contextual links from high-traffic posts to commercial pages
3. Optimize anchor text on key navigation links

### P2 (This Month)

1. Audit and update all internal links site-wide
2. Implement related posts section on blog templates
3. Add breadcrumb navigation

### P3 (Ongoing)

1. Add 3-5 internal links when publishing new content
2. Quarterly orphan page audits
3. Monitor and fix broken links monthly

### 빠른 판단 기준

- P0 (Immediate)는 orphan pages와 broken links를 즉시 해결한다
- P1 (This Week)는 pillar-cluster structure와 contextual links를 구축한다
- P2 (This Month)는 site-wide audit과 breadcrumbs를 추가한다
- P3 (Ongoing)는 새 콘텐츠에 internal links를 추가하고 monthly audit을 수행한다
- Priority 순서로 진행하면 quick wins를 먼저 확보한다

---

## 7. Quick Wins

1. **Add links from high-traffic pages** — top 10 traffic pages에 conversion target 페이지 링크 추가
2. **Fix orphan pages** — traffic 있는 orphan pages 에 즉시 링크 추가
3. **Optimize homepage links** — homepage 에서 commercial pages 로 직접 링크
4. **Add contextual links** — "click here"를 descriptive anchor 로 교체
5. **Create topic clusters** — main topics 에 대해 pillar-cluster 구조 구축
### 빠른 판단 기준

- High-traffic pages에서 conversion target pages로 링크를 추가한다
- Orphan pages with traffic을 즉시 해결한다
- Homepage에서 commercial pages로 직접 링크를 추가한다
- "click here"를 descriptive anchor로 교체한다
- Main topics에 pillar-cluster 구조를 구축한다
---

## 8. Tools and Automation

### Crawl Tools

- Screaming Frog: site-wide link analysis
- Ahrefs Site Audit: internal link reports
- Google Search Console: internal links report

### Automation Scripts

- Find orphan pages: crawl site and identify pages with zero internal links
- Link opportunity finder: scan content for keyword mentions that could link to relevant pages
- Broken link checker: identify and report broken internal links

### 빠른 판단 기준

- Screaming Frog는 site-wide link analysis에 필수다
- Ahrefs Site Audit은 internal link reports를 제공한다
- Google Search Console은 internal links report를 확인한다
- Orphan pages finder는 zero internal links를 식별한다
- Link opportunity finder는 keyword mentions에서 link opportunities를 찾다

---

## 9. Measurement and Monitoring

### Metrics to Track

| Metric | Target | Frequency |
|--------|--------|-----------|
| Orphan pages | 0 | Monthly |
| Average links per page | 5-15 | Monthly |
| Click depth to important pages | <3 clicks | Quarterly |
| Internal link CTR | >2% | Weekly |
| Broken internal links | 0 | Weekly |

### Success Signals

- Orphan page count decreases over time
- Important commercial pages receive more internal links
- Crawl depth to key pages is reduced
- Organic traffic to previously orphan pages increases
- Overall site authority distribution improves

### 빠른 판단 기준

- Orphan pages는 target 0, monthly로 tracking한다
- Average links per page는 5-15, monthly로 tracking한다
- Click depth to important pages는 <3 clicks, quarterly로 tracking한다
- Internal link CTR은 >2%, weekly로 tracking한다
- Broken internal links는 target 0, weekly로 tracking한다
- Success signals가 positive trend를 보이면 internal linking strategy가 작동한다
