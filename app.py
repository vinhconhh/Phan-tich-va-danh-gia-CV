import streamlit as st
import pandas as pd
from services.extractor import extract_text
from services.classifier import classify_cv
from services.infor_extractor import extract_info
from services.matcher import rank_multiple_cvs
from services.score import score_cv

st.set_page_config(page_title="Phân tích và đánh giá CV", page_icon="📄", layout="wide")
st.title("🎯 Phân tích, trích xuất, so khớp và đánh giá CV (SBERT)")

# ==================== INPUT ====================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload CV (nhiều file)")
    uploaded_files = st.file_uploader(
        ".", type=["pdf", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

with col2:
    st.subheader("💼 Job Description")
    jd_text = st.text_area(
        ".", height=200,
        placeholder="Nhập mô tả công việc...",
        label_visibility="collapsed"
    )

# ==================== ANALYZE ====================
if st.button("🚀 Phân Tích CV", type="primary", use_container_width=True):

    if not uploaded_files:
        st.error("Vui lòng upload ít nhất 1 CV")
        st.stop()

    with st.spinner("Đang phân tích..."):
        cv_texts = {f.name: extract_text(f) for f in uploaded_files}
        classify_results = {n: classify_cv(t)    for n, t in cv_texts.items()}
        extract_results  = {n: extract_info(t)   for n, t in cv_texts.items()}
        score_results    = {n: score_cv(t, extract_results[n]) for n, t in cv_texts.items()}

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
            clf = classify_results[name]
            st.subheader(name)
            c1, c2 = st.columns(2)
            c1.metric("Danh mục", clf["category"])
            c2.metric("Độ tin cậy", f"{clf['confidence']}%")
            st.subheader("Chi tiết phân loại (%)")
            st.bar_chart(clf["all_scores"])
            st.divider()

    # ==================== TAB 2 ====================
    with tab2:
        st.header("2. Trích Xuất Thông Tin")

        # ── Bảng tổng hợp tất cả CV ──
        rows = []
        for name in cv_texts:
            info = extract_results[name]
            rows.append({
                "📄 File":        name,
                "👤 Họ tên":      info.get("name", "N/A"),
                "📧 Email":       info.get("email", "N/A"),
                "📞 Điện thoại":  info.get("phone", "N/A"),
                "🎓 Học vấn":     "\n".join(info.get("education", [])) or "N/A",
                "💼 Kinh nghiệm": "\n".join(info.get("experience", [])) or "N/A",
                "🛠️ Kỹ năng":    ", ".join(info.get("skills", [])) or "N/A",
            })

        df_summary = pd.DataFrame(rows)

        st.subheader("📊 Bảng tổng hợp")
        st.dataframe(
            df_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "📄 File":        st.column_config.TextColumn(width="medium"),
                "👤 Họ tên":      st.column_config.TextColumn(width="small"),
                "📧 Email":       st.column_config.TextColumn(width="medium"),
                "📞 Điện thoại":  st.column_config.TextColumn(width="small"),
                "🎓 Học vấn":     st.column_config.TextColumn(width="large"),
                "💼 Kinh nghiệm": st.column_config.TextColumn(width="large"),
                "🛠️ Kỹ năng":    st.column_config.TextColumn(width="medium"),
            }
        )

        # Nút export Excel
        import io
        df_export = pd.DataFrame([{
            "File":        r["📄 File"],
            "Họ tên":      r["👤 Họ tên"],
            "Email":       r["📧 Email"],
            "Điện thoại":  r["📞 Điện thoại"],
            "Học vấn":     r["🎓 Học vấn"],
            "Kinh nghiệm": r["💼 Kinh nghiệm"],
            "Kỹ năng":     r["🛠️ Kỹ năng"],
        } for r in rows])

        # Xoá ký tự đặc biệt mà openpyxl không chấp nhận
        import re as _re
        def clean_for_excel(val):
            if not isinstance(val, str):
                return val
            # Xoá control characters (trừ tab, newline hợp lệ)
            val = _re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", val)
            # Thay newline bằng space để hiển thị gọn trong 1 ô
            val = val.replace("\n", " | ")
            return val

        df_export = df_export.applymap(clean_for_excel)

        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            df_export.to_excel(writer, index=False, sheet_name="CV Data")
        st.download_button(
            label="⬇️ Tải xuống Excel",
            data=buf.getvalue(),
            file_name="cv_extracted.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.divider()

        # ── Chi tiết từng CV ──
        st.subheader("🔎 Chi tiết từng CV")
        for name in cv_texts:
            info = extract_results[name]
            with st.expander(f"📄 {name}", expanded=False):

                # Thông tin cá nhân
                df_personal = pd.DataFrame([{
                    "Họ tên":     info.get("name", "N/A"),
                    "Email":      info.get("email", "N/A"),
                    "Điện thoại": info.get("phone", "N/A"),
                }])
                st.markdown("**👤 Cá nhân**")
                st.dataframe(df_personal, use_container_width=True, hide_index=True)

                # Học vấn
                if info.get("education"):
                    st.markdown("**🎓 Học vấn**")
                    for line in info["education"]:
                        st.markdown(f"- {line}")

                # Kinh nghiệm
                if info.get("experience"):
                    st.markdown("**💼 Kinh nghiệm**")
                    for line in info["experience"]:
                        st.markdown(f"- {line}")

                # Kỹ năng
                if info.get("skills"):
                    st.markdown("**🛠️ Kỹ năng**")
                    skills = info["skills"]
                    # Chia thành 4 cột
                    cols = st.columns(4)
                    for i, skill in enumerate(skills):
                        cols[i % 4].markdown(
                            f'<span style="background:#1f4287;color:white;'
                            f'padding:3px 10px;border-radius:12px;'
                            f'font-size:13px">{skill}</span>',
                            unsafe_allow_html=True
                        )

    # ==================== TAB 3 ====================
    with tab3:
        st.header("3. So Khớp JD - CV")
        if not jd_text.strip():
            st.warning("Vui lòng nhập Job Description để xem kết quả so khớp")
        else:
            ranking = rank_multiple_cvs(cv_texts, jd_text)

            # Bảng ranking
            df_rank = pd.DataFrame([
                {"Hạng": i+1, "File CV": name, "Độ phù hợp (%)": score}
                for i, (name, score) in enumerate(ranking)
            ])
            st.dataframe(df_rank, use_container_width=True, hide_index=True,
                         column_config={
                             "Hạng": st.column_config.NumberColumn(width="small"),
                             "Độ phù hợp (%)": st.column_config.ProgressColumn(
                                 min_value=0, max_value=100, format="%.1f%%"
                             )
                         })

    # ==================== TAB 4 ====================
    with tab4:
        st.header("4. Đánh Giá Tổng Thể")
        weights = {"skills": 30, "experience": 30, "education": 15, "length": 10, "keywords": 15}

        # Bảng tổng hợp điểm
        score_rows = []
        for name in cv_texts:
            s = score_results[name]
            row = {"File CV": name, "Tổng điểm": s["total_score"]}
            for k, w in weights.items():
                row[k.upper()] = f"{round(s['breakdown'][k]*w)}/{w}"
            score_rows.append(row)

        df_scores = pd.DataFrame(score_rows)
        st.dataframe(
            df_scores,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Tổng điểm": st.column_config.ProgressColumn(
                    min_value=0, max_value=100, format="%d/100"
                )
            }
        )