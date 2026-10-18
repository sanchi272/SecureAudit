
import streamlit as st

st.set_page_config(
    page_title="SecureAudit",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 SecureAudit")
st.subheader("Information Security Audit and Risk Assessment System")

st.write(
    "Assess security controls, identify potential risks, "
    "and get recommendations to improve information security."
)

st.info("Welcome! Use the sidebar to explore the security assessment modules.")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Asset Classification",
        "Security Audit",
        "Risk Assessment",
        "Access Control Review",
        "Security Recommendations",
        "Audit Report"
    ]
)

if page == "Home":
    st.header("Project Overview")
    st.write("SecureAudit helps users assess basic security controls.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Main Modules", "6")
    col2.metric("Assessment Type", "Checklist")
    col3.metric("Risk Levels", "4")


elif page == "Asset Classification":
    st.header("🖥️ Asset Classification")
    st.write("Add an asset and classify its importance.")

    with st.form("asset_form"):
        asset_name = st.text_input(
            "Asset Name",
            placeholder="e.g. College Student Database"
        )

        asset_type = st.selectbox(
            "Asset Type",
            ["Computer System", "User Account", "Database",
             "Document", "Network Device", "Other"]
        )

        importance = st.selectbox(
            "Asset Importance",
            ["Low", "Medium", "High", "Critical"]
        )

        submitted = st.form_submit_button("Add Asset")

    if "assets" not in st.session_state:
        st.session_state.assets = []

    if submitted:
        if asset_name.strip():
            st.session_state.assets.append({
                "Asset Name": asset_name.strip(),
                "Asset Type": asset_type,
                "Importance": importance
            })
            st.success("Asset added successfully!")
        else:
            st.warning("Please enter an asset name.")

    if st.session_state.assets:
        st.subheader("Classified Assets")
        st.dataframe(
            st.session_state.assets,
            use_container_width=True
        )
        st.write("Total Assets:", len(st.session_state.assets))



elif page == "Security Audit":
    st.header("🔍 Security Audit Checklist")
    st.write("Review the security controls of your organization.")

    questions = {
        "Strong password policy is implemented": "Password Policy",
        "Regular data backups are maintained": "Data Backup",
        "Software is regularly updated": "Software Updates",
        "User access is restricted by role": "Access Control",
        "Security logs are regularly monitored": "Log Monitoring",
        "Antivirus or equivalent protection is enabled": "Malware Protection",
        "Sensitive data is protected": "Data Protection",
        "Security incidents are documented": "Incident Reporting"
    }

    with st.form("audit_form"):
        answers = {}

        for question, key in questions.items():
            answers[key] = st.radio(
                question,
                ["Yes", "No"],
                horizontal=True,
                key=f"audit_{key}"
            )

        submitted = st.form_submit_button("Run Security Audit")

    if submitted:
        passed = sum(1 for answer in answers.values() if answer == "Yes")
        total = len(answers)
        percentage = (passed / total) * 100

        st.session_state.audit_results = {
            key: answer for key, answer in answers.items()
        }
        st.session_state.audit_percentage = percentage

        st.subheader("Audit Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Controls", total)
        col2.metric("Satisfactory Controls", passed)
        col3.metric("Compliance", f"{percentage:.1f}%")

        st.progress(percentage / 100)

        st.write("### Control-wise Findings")

        for key, answer in answers.items():
            if answer == "Yes":
                st.success(f"{key}: Satisfactory")
            else:
                st.warning(f"{key}: Improvement Required")



elif page == "Risk Assessment":
    st.header("⚠️ Risk Assessment Calculator")
    st.write("Evaluate potential security risks.")

    with st.form("risk_form"):
        risk_name = st.text_input(
            "Risk Name",
            placeholder="e.g. Data Loss"
        )

        likelihood = st.slider(
            "Likelihood (1 = Very Low, 5 = Very High)",
            min_value=1,
            max_value=5,
            value=3
        )

        impact = st.slider(
            "Impact (1 = Very Low, 5 = Very High)",
            min_value=1,
            max_value=5,
            value=3
        )

        submitted = st.form_submit_button("Calculate Risk")

    if "risk_records" not in st.session_state:
        st.session_state.risk_records = []

    if submitted:
        if risk_name.strip():
            score = likelihood * impact

            if score <= 4:
                level = "Low"
            elif score <= 9:
                level = "Medium"
            elif score <= 15:
                level = "High"
            else:
                level = "Critical"

            record = {
                "Risk": risk_name.strip(),
                "Likelihood": likelihood,
                "Impact": impact,
                "Risk Score": score,
                "Risk Level": level
            }

            st.session_state.risk_records.append(record)

            st.subheader("Risk Assessment Result")
            st.metric("Risk Score", f"{score}/25")
            st.write(f"**Risk Level:** {level}")

            if level == "Low":
                st.success("Continue routine monitoring.")
            elif level == "Medium":
                st.info("Review existing security controls.")
            elif level == "High":
                st.warning("Plan corrective security measures.")
            else:
                st.error("Prioritize risk mitigation measures.")
        else:
            st.warning("Please enter a risk name.")

    if st.session_state.risk_records:
        st.subheader("Risk Register")
        st.dataframe(
            st.session_state.risk_records,
            use_container_width=True
        )

elif page == "Access Control Review":
    st.header("👤 Access Control Review")
    st.write("Simulate role-based access permissions.")

    permissions = {
        "Admin": ["Dashboard", "User Management", "Audit Reports", "Settings"],
        "Staff": ["Dashboard", "Audit Reports"],
        "Guest": ["Dashboard"]
    }

    role = st.selectbox(
        "Select User Role",
        ["Admin", "Staff", "Guest"]
    )

    resource = st.selectbox(
        "Select Resource",
        ["Dashboard", "User Management", "Audit Reports", "Settings"]
    )

    if st.button("Check Access"):
        if resource in permissions[role]:
            st.success(f"ACCESS GRANTED: {role} can access {resource}.")
        else:
            st.error(f"ACCESS DENIED: {role} cannot access {resource}.")

    st.subheader("Role Permissions Table")

    permission_rows = []

    for user_role, allowed_resources in permissions.items():
        for item in [
            "Dashboard", "User Management",
            "Audit Reports", "Settings"
        ]:
            permission_rows.append({
                "Role": user_role,
                "Resource": item,
                "Permission": (
                    "Allowed"
                    if item in allowed_resources
                    else "Denied"
                )
            })

    st.dataframe(permission_rows, use_container_width=True)



elif page == "Security Recommendations":
    st.header("🛡️ Security Recommendations")
    st.write("Review common security risks and recommended countermeasures.")

    recommendations = {
        "Weak Password Policy": {
            "Risk": "Unauthorized account access",
            "Action": "Enforce strong passwords and multi-factor authentication."
        },
        "No Regular Data Backup": {
            "Risk": "Data loss or service disruption",
            "Action": "Maintain regular backups and test data recovery."
        },
        "Outdated Software": {
            "Risk": "Known security vulnerabilities",
            "Action": "Apply approved software updates regularly."
        },
        "Excessive User Permissions": {
            "Risk": "Unauthorized access to sensitive information",
            "Action": "Apply role-based access and least privilege."
        },
        "Unmonitored Security Logs": {
            "Risk": "Suspicious activities may go unnoticed",
            "Action": "Review logs regularly and investigate unusual events."
        },
        "Insufficient Data Protection": {
            "Risk": "Sensitive information may be exposed",
            "Action": "Use appropriate encryption and restrict data access."
        },
        "No Incident Response Plan": {
            "Risk": "Delayed response to security incidents",
            "Action": "Document incident handling and reporting procedures."
        }
    }

    selected_issue = st.selectbox(
        "Select a Security Issue",
        list(recommendations.keys())
    )

    if st.button("Get Recommendation"):
        details = recommendations[selected_issue]

        st.subheader("Assessment")
        st.write("**Security Issue:**", selected_issue)
        st.write("**Potential Risk:**", details["Risk"])
        st.success("**Recommended Action:** " + details["Action"])

    st.divider()
    st.subheader("Security Best Practices")

    st.markdown("""
    - Use strong authentication and appropriate access permissions.
    - Keep software and security controls updated.
    - Maintain regular backups.
    - Protect sensitive information.
    - Monitor security logs.
    - Document security incidents.
    - Review security policies regularly.
    """)


elif page == "Audit Report":
    st.header("📊 Security Audit Report")
    st.write("Summary of the current security assessment.")

    import pandas as pd

    audit_results = st.session_state.get("audit_results", {})
    audit_percentage = st.session_state.get("audit_percentage", None)
    risk_records = st.session_state.get("risk_records", [])
    assets = st.session_state.get("assets", [])

    st.subheader("Assessment Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Assets Classified", len(assets))
    col2.metric("Risks Identified", len(risk_records))

    if audit_percentage is not None:
        col3.metric("Audit Compliance", f"{audit_percentage:.1f}%")
    else:
        col3.metric("Audit Compliance", "Not assessed")

    st.divider()

    st.subheader("Asset Register")
    if assets:
        st.dataframe(pd.DataFrame(assets), use_container_width=True)
    else:
        st.info("No assets have been classified yet.")

    st.subheader("Security Audit Findings")
    if audit_results:
        audit_rows = []

        for control, answer in audit_results.items():
            audit_rows.append({
                "Security Control": control,
                "Status": (
                    "Satisfactory"
                    if answer == "Yes"
                    else "Improvement Required"
                )
            })

        st.dataframe(pd.DataFrame(audit_rows), use_container_width=True)
    else:
        st.info("Complete the Security Audit first.")

    st.subheader("Risk Register")
    if risk_records:
        st.dataframe(pd.DataFrame(risk_records), use_container_width=True)
    else:
        st.info("No risks have been assessed yet.")

    report_rows = []

    for asset in assets:
        report_rows.append({
            "Section": "Asset",
            "Item": asset["Asset Name"],
            "Details": f'Type: {asset["Asset Type"]}; Importance: {asset["Importance"]}'
        })

    for control, answer in audit_results.items():
        report_rows.append({
            "Section": "Security Audit",
            "Item": control,
            "Details": "Satisfactory" if answer == "Yes" else "Improvement Required"
        })

    for risk in risk_records:
        report_rows.append({
            "Section": "Risk Assessment",
            "Item": risk["Risk"],
            "Details": f'Score: {risk["Risk Score"]}; Level: {risk["Risk Level"]}'
        })

    if report_rows:
        report_df = pd.DataFrame(report_rows)
        csv_data = report_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Audit Report (CSV)",
            data=csv_data,
            file_name="SecureAudit_Report.csv",
            mime="text/csv"
        )
    else:
        st.warning("Add assets, complete an audit, or assess a risk to generate a report.")

