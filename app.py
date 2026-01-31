import streamlit as st
from services.extractor import extract_text
from services.classifier import classify_cv
from services.infor_extractor import extract_info
from services.matcher import rank_multiple_cvs
from services.score import score_cv

# ==================== CONFIG ====================
st.set_page_config(
    page_title="Phân tích và đánh giá CV",
    page_icon="📄",
    layout="wide"
)

st.title("🎯 Phân tích, trích xuất, so khớp và đánh giá CV (SBERT)")

# ==================== INPUT ====================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload CV (nhiều file)")
    uploaded_files = st.file_uploader(
        ".",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

with col2:
    st.subheader("💼 Job Description")
    jd_text = st.text_area(
        ".",
        height=200,
        placeholder="Nhập mô tả công việc...",
        label_visibility="collapsed"
    )

# ==================== ANALYZE ====================
if st.button("🚀 Phân Tích CV", type="primary", use_container_width=True):

    if not uploaded_files:
        st.error("Vui lòng upload ít nhất 1 CV")
        st.stop()

    with st.spinner("Đang phân tích..."):
        cv_texts = {}
        for f in uploaded_files:
            cv_texts[f.name] = extract_text(f)

        # ---- xử lý 1 lần, lưu kết quả ----
        classify_results = {}
        extract_results = {}
        score_results = {}

        for name, text in cv_texts.items():
            classify_results[name] = classify_cv(text)
            extract_results[name] = extract_info(text)
            score_results[name] = score_cv(text, extract_results[name])

    # ==================== TABS ====================
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏷️ Phân loại",
        "📋 Trích xuất thông tin",
        "🔍 So khớp JD-CV",
        "⭐ Đánh giá"
    ])

    # ==================== TAB 1 ====================
    with tab1:
        st.header("1. Phân Loại CV")

        for name in cv_texts:
            classification = classify_results[name]

            st.subheader(name)
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Danh mục", classification["category"])
            with c2:
                st.metric("Độ tin cậy", f"{classification['confidence']}%")

            st.subheader("Chi tiết phân loại (%)")
            st.bar_chart(classification["all_scores"])
            st.divider()

    # ==================== TAB 2 ====================
    with tab2:
        st.header("2. Trích Xuất Thông Tin")

        for name in cv_texts:
            info = extract_results[name]

            st.subheader(name)
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("👤 Cá nhân")
                st.write(f"**Họ tên:** {info.get('name','N/A')}")
                st.write(f"**Email:** {info.get('email','N/A')}")
                st.write(f"**Điện thoại:** {info.get('phone','N/A')}")

            with col2:
                st.subheader("🎓 Học vấn")
                for edu in info.get("education", []):
                    st.write(f"- {edu}")

            st.subheader("💼 Kinh nghiệm")
            for exp in info.get("experience", []):
                st.write(f"- {exp}")

            st.subheader("🛠️ Kỹ năng")
            cols = st.columns(4)
            for idx, skill in enumerate(info.get("skills", [])):
                st.button(skill, disabled=True, key=f"{name}_{skill}_{idx}")

            st.divider()

    # ==================== TAB 3 ====================
    with tab3:
        st.header("3. So Khớp JD - CV (SBERT)")

        if not jd_text.strip():
            st.warning("Vui lòng nhập Job Description")
            st.stop()

        ranking = rank_multiple_cvs(cv_texts, jd_text)

        for name, score in ranking:
            st.subheader(name)
            st.progress(score / 100)
            st.metric("Độ phù hợp", f"{score}%")

    # ==================== TAB 4 ====================
    with tab4:
        st.header("4. Đánh Giá Tổng Thể")

        for name, text in cv_texts.items():
            info = extract_info(text)
            scoring = score_cv(text, info)

            st.subheader(name)

            # Tổng điểm
            st.metric("Điểm CV", f"{scoring['total_score']}/100")
            st.progress(scoring["total_score"] / 100)

            st.markdown("### Chi tiết điểm")
            for k, v in scoring["breakdown"].items():
                real = round(v["score"] * v["weight"])
                st.write(f"**{k.upper()}** ({v['weight']}%) : {real}/{v['weight']}")

            st.divider()