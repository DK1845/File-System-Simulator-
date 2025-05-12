import streamlit as st
from file_manager import create_file, delete_file, get_all_files, get_file_content, update_file_content
from visualization import show_disk

# Set up page configuration
st.set_page_config(page_title="File System Simulator", layout="wide")

st.markdown("""
    <h1 style='text-align: center;'>📁 File System Simulator</h1>
    <p style='text-align: center; font-size:18px;'>Visualize how file systems work using different disk allocation strategies.</p>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# Define function to show the file creation page
def create_file_page():
    st.subheader("📝 Create a New File")
    with st.form("create_file_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            file_name = st.text_input("📁 File Name")
        with col2:
            file_size = st.number_input("📦 File Size (in blocks)", min_value=1, max_value=100, step=1)
        with col3:
            method = st.selectbox("⚙️ Allocation Method", ["Contiguous", "Linked", "Indexed"])

        # File content (only text)
        content = st.text_area("📝 File Content", height=150)

        submitted = st.form_submit_button("➕ Create File", use_container_width=True)
        if submitted:
            if file_name:
                if create_file(file_name, file_size, method, 'Text', content):
                    st.success(f"✅ File '{file_name}' created using **{method}** allocation.")
                else:
                    st.error("❌ Not enough space or fragmentation issue.")
            else:
                st.warning("⚠️ Please enter a file name.")


# Define function to show the file directory page
def view_files_page():
    st.subheader("📄 File Directory")
    file_data = get_all_files()
    if file_data:
        for name, info in file_data.items():
            with st.expander(f"📂 {name} | Method: {info['method']}", expanded=False):
                st.markdown(f"""
                    <ul>
                        <li><strong>Size:</strong> {info['size']} blocks</li>
                        <li><strong>Allocated Blocks:</strong> {info['blocks']}</li>
                        {f"<li><strong>Index Block:</strong> {info['index']}</li>" if info['method'] == 'Indexed' else ""}
                    </ul>
                """, unsafe_allow_html=True)

                # Display file content (Only Text Content)
                st.write(info['content'])
    else:
        st.info("🪶 No files created yet.")


# Define function to show the file deletion page
def delete_file_page():
    st.subheader("🗑️ Delete Files")
    file_list = list(get_all_files().keys())
    if file_list:
        with st.expander("🔻 Select and delete one or more files", expanded=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                selected_files = st.multiselect("Select files to delete", file_list)
            with col2:
                if st.button("🧺 Delete Selected", use_container_width=True):
                    if selected_files:
                        for f in selected_files:
                            delete_file(f)
                        st.success(f"✅ Deleted files: {', '.join(selected_files)}")
                    else:
                        st.warning("⚠️ Please select at least one file.")
    else:
        st.info("📂 No files currently available for deletion.")


# Define function to show the file editing page
def edit_file_page():
    st.subheader("✏️ Edit File Content")
    editable_files = list(get_all_files().keys())
    if editable_files:
        file_to_edit = st.selectbox("Select a file to edit", editable_files)

        if file_to_edit:
            # Only show the text area and save button when a file is selected
            current_content = get_file_content(file_to_edit)

            if current_content and isinstance(current_content, str):  # Only show text editor for text files
                new_content = st.text_area("📝 File Editor", value=current_content, height=200)

                if st.button("💾 Save Changes"):
                    update_file_content(file_to_edit, new_content)
                    st.success(f"📝 Content of '{file_to_edit}' updated.")
            else:
                st.warning("🖼️ Cannot edit non-text files.")
    else:
        st.info("📂 No files available to edit.")


# Define function to show the disk visualization page
def disk_visualization_page():
    st.subheader("📊 Disk Usage Visualization")
    st.markdown("Color-coded chart shows how blocks are allocated.")
    fig = show_disk()
    st.pyplot(fig)


# Main Page Navigation
def main():
    pages = ["Create File", "View Files", "Edit File", "Delete File", "Disk Visualization"]
    selected_page = st.sidebar.radio("Select a Page", pages)

    if selected_page == "Create File":
        create_file_page()
    elif selected_page == "View Files":
        view_files_page()
    elif selected_page == "Edit File":
        edit_file_page()
    elif selected_page == "Delete File":
        delete_file_page()
    elif selected_page == "Disk Visualization":
        disk_visualization_page()


# Run the main function
if __name__ == "__main__":
    main()
