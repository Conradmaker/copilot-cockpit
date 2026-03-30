# 영문 AI 작문 패턴 감지·교정 가이드 (17종)

Wikipedia의 "Signs of AI writing" 가이드(WikiProject AI Cleanup)와 humanizer 스킬에 기반한 영문 AI 패턴 목록이다. 각 패턴마다 **감지 기준**(어떤 단어·구문·구조가 AI 패턴인지), **교정 전략**(어떻게 자연스럽게 고치는지), Before/After 예시를 포함한다.

---

## 콘텐츠 패턴 (Content Patterns)

### 패턴 1: 과잉 의미·유산·틀 부여 (Undue Emphasis on Significance)

**감지 기준**:
- 다음 단어·구문이 보이면 의심: stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted
- 사실에 비해 의미를 과도하게 부풀리는 서술

**교정 전략**:
- 과잉 의미 부여 구문을 제거하고 사실만 남긴다
- "pivotal moment in the evolution of"를 구체적 사실로 교체한다
- 무엇이 실제로 일어났는지만 기술한다

**Before**:
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions.

**After**:
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

---

### 패턴 2: 과잉 주목성·미디어 언급 (Undue Emphasis on Notability)

**감지 기준**:
- 다음 구문이 보이면 의심: independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence
- 맥락 없이 미디어 소스를 나열하거나 주목성을 강조

**교정 전략**:
- 미디어 소스 나열 대신 구체적 인용 하나와 맥락을 제공한다
- "active social media presence"같은 주목성 주장을 삭제하고 실제 발언이나 사실로 교체한다

**Before**:
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After**:
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

---

### 패턴 3: 표면적 -ing 분석 (Superficial -ing Analyses)

**감지 기준**:
- 문장 끝에 현재분사(-ing)구가 부가적 의미처럼 붙는 패턴
- 주의 단어: highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, cultivating, fostering, encompassing, showcasing

**교정 전략**:
- -ing구를 삭제하고, 실제로 전달하는 정보가 있으면 별도 문장으로 독립시킨다
- 대부분 삭제만 해도 의미가 보존된다

**Before**:
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After**:
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

---

### 패턴 4: 판촉·광고성 언어 (Promotional Language)

**감지 기준**:
- 주의 단어: boasts a, vibrant, rich (비유적), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (비유적), renowned, breathtaking, must-visit, stunning
- 중립적 서술이어야 할 곳에 감탄사나 판촉 수식어가 들어감

**교정 전략**:
- 판촉 형용사를 모두 삭제하거나 관찰 가능한 사실로 교체한다
- "nestled in the breathtaking region"을 단순 위치 정보로 바꾼다

**Before**:
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After**:
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

---

### 패턴 5: 모호한 귀속·위즐 워드 (Vague Attributions)

**감지 기준**:
- 주의 구문: Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (출처 미명시)
- 구체적 출처 없이 "전문가"나 "관찰자"를 인용

**교정 전략**:
- 모호한 귀속을 구체적 출처(이름, 연도, 기관)로 교체한다
- 출처를 찾을 수 없으면 해당 주장 자체를 삭제한다

**Before**:
> Experts believe it plays a crucial role in the regional ecosystem.

**After**:
> The river supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

---

### 패턴 6: 공식적 "도전과 전망" 섹션 (Challenges and Future Prospects)

**감지 기준**:
- 다음 패턴으로 시작하는 섹션: "Despite its... faces several challenges...", "Despite these challenges", "Challenges and Legacy", "Future Outlook"
- 구체적 데이터 없이 도전과 낙관을 공식적으로 나열

**교정 전략**:
- 공식을 깨고 구체적 사례, 데이터, 타임라인으로 교체한다
- "Despite these challenges, it continues to thrive"를 실제 변화나 프로젝트로 대체한다

**Before**:
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, Korattur continues to thrive as an integral part of Chennai's growth.

**After**:
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

---

## 언어·문법 패턴 (Language & Grammar Patterns)

### 패턴 7: AI 유행어 과다 사용 (Overused AI Vocabulary)

**감지 기준 — 주의 단어 목록**:
- 고빈도: Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (동사), interplay, intricate/intricacies, key (형용사), landscape (추상 명사), pivotal, showcase, tapestry (추상 명사), testament, underscore (동사), valuable, vibrant
- 이 단어들이 한 단락에 2개 이상 동시에 나타나면 AI 패턴 확률이 높다

**교정 전략**:
- 각 단어를 문맥에 맞는 구체적 표현으로 교체한다
- "delve into" → "examine", "look at", "explore"
- "leverage" → "use"
- "foster" → 구체적 행동 (fund, teach, build)
- "landscape" → 구체적 영역 이름
- "tapestry" → 삭제하거나 구체적 구성 요소 나열

**Before**:
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After**:
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

---

### 패턴 8: Copula 회피 (Avoidance of "is"/"are")

**감지 기준**:
- 주의 구문: serves as, stands as, marks, represents [a], boasts, features, offers [a]
- 단순한 "is"/"are"로 충분한 곳에 복잡한 동사를 사용

**교정 전략**:
- "serves as"를 "is"로, "boasts"를 "has"로, "features"를 "has"/"includes"로 교체한다

**Before**:
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After**:
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

---

### 패턴 9: 부정 평행구문 (Negative Parallelisms)

**감지 기준**:
- "Not only...but...", "It's not just about..., it's...", "It's not merely a..., it's a..."
- 같은 글에서 이 구문이 반복적으로 나타남

**교정 전략**:
- 부정 평행구문을 삭제하고 핵심 주장만 직접 서술한다
- 한 번만 쓰는 것은 수사법이지만, 반복되면 AI 패턴이다

**Before**:
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After**:
> The heavy beat adds to the aggressive tone.

---

### 패턴 10: 3박자 과용 (Rule of Three Overuse)

**감지 기준**:
- 3개 항목 목록이 한 글에서 반복적으로 나타남
- "innovation, inspiration, and industry insights" 같은 추상적 3박자

**교정 전략**:
- 일부를 2항목이나 4항목으로 바꾼다
- 추상적 3박자는 구체적 사실로 교체한다

**Before**:
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After**:
> The event includes talks and panels. There's also time for informal networking between sessions.

---

### 패턴 11: 동의어 순환 (Elegant Variation / Synonym Cycling)

**감지 기준**:
- 같은 대상을 가리키면서 매 문장마다 다른 이름을 사용
- protagonist → main character → central figure → hero

**교정 전략**:
- 하나의 명칭을 선택하고 일관되게 사용한다. 반복이 두려우면 대명사를 쓴다

**Before**:
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After**:
> The protagonist faces many challenges but eventually triumphs and returns home.

---

### 패턴 12: 가짜 범위 (False Ranges)

**감지 기준**:
- "from X to Y" 구문에서 X와 Y가 의미 있는 스케일 위에 있지 않음
- "from the singularity of the Big Bang to the grand cosmic web"

**교정 전략**:
- 가짜 범위를 구체적 주제 나열로 교체한다

**Before**:
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After**:
> The book covers the Big Bang, star formation, and current theories about dark matter.

---

## 스타일 패턴 (Style Patterns)

### 패턴 13: Em dash 남용

**감지 기준**:
- 한 문단에 em dash(—)가 3개 이상
- 쉼표나 마침표로 충분한 곳에 em dash 사용

**교정 전략**:
- 대부분의 em dash를 쉼표, 마침표, 또는 괄호로 교체한다
- 한 문단에 em dash는 최대 1–2개로 제한한다

**Before**:
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.

**After**:
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

---

### 패턴 14: 볼드체 남용 (Overuse of Boldface)

**감지 기준**:
- 문장 안에서 핵심이 아닌 약어, 제목, 도구 이름을 기계적으로 볼드 처리
- 한 문단에 볼드가 3군데 이상이면 의심

**교정 전략**:
- 볼드를 모두 제거하고, 진짜 강조가 필요한 곳(첫 등장 정의, 경고)에만 살린다

**Before**:
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After**:
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

---

### 패턴 15: 인라인 헤더 수직 목록 (Inline-Header Vertical Lists)

**감지 기준**:
- 불릿 리스트 각 항목이 **볼드 헤더:** + 설명 형식
- 실제로는 한 문단으로 충분한 내용을 기계적으로 리스트화

**교정 전략**:
- 항목 수가 3개 이하이고 각각 한 줄이면 문장으로 합친다
- 정말 스캔이 필요한 긴 목록에만 이 형식을 유지한다

**Before**:
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After**:
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

---

### 패턴 16: 제목 Title Case 과용

**감지 기준**:
- 모든 주요 단어를 대문자로 시작하는 제목 (Title Case)
- 문서 내 모든 제목이 빠짐없이 Title Case

**교정 전략**:
- 첫 단어와 고유명사만 대문자로 쓰는 Sentence case로 교체한다
- 프로젝트 스타일 가이드가 Title Case를 요구하면 그것을 따른다

**Before**:
> ## Strategic Negotiations And Global Partnerships

**After**:
> ## Strategic negotiations and global partnerships

---

### 패턴 17: 이모지 장식 (Emoji Decoration)

**감지 기준**:
- 제목이나 불릿 앞에 이모지가 장식처럼 붙어 있음
- 🚀, 💡, ✅, 📊, 🎯 등이 정보 없이 시각적 장식만 수행

**교정 전략**:
- 이모지를 모두 삭제하고, 내용의 명확성으로 구조를 전달한다
- 이모지가 의미를 전달하는 경우(상태 표시 등)에만 유지한다

**Before**:
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting

**After**:
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

---

## 보이스와 성격 주입

AI 패턴을 제거하는 것만으로는 부족하다. 깨끗하지만 무미건조한 글도 AI처럼 느껴진다.

### 무미건조한 글의 신호

- 모든 문장이 같은 길이와 구조
- 의견, 감정, 불확실성 없이 중립적 보고만
- 1인칭 없음, 질문 없음
- 유머나 날카로움 없음
- 위키피디아 기사나 보도자료처럼 읽힘

### 교정 전략

- 의견을 넣는다: "I genuinely don't know how to feel about this"
- 리듬을 변주한다: 짧고 강렬한 문장. 그리고 때로는 길게 풀어쓰는 문장
- 복잡한 감정을 인정한다: "impressive but also unsettling"
- 적절한 곳에 1인칭을 쓴다: "I keep coming back to..."
- 약간의 불완전함을 허용한다: 탈선, 곁다리, 반쯤 형성된 생각

**Before** (깨끗하지만 무미건조):
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

**After** (목소리가 있는):
> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept. Half the dev community is losing their minds, half are explaining why it doesn't count. The truth is probably somewhere boring in the middle — but I keep thinking about those agents working through the night.
