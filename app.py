import streamlit as st
from scanner import ping_sweep
from todo import load_todos, add_todo, remove_todo, update_todo
from datetime import date, datetime
def todo_app():
    st.header("📝 To-Do List Manager")
    
    # Initialize session_state keys
    todos = load_todos()
    for todo in todos:
        task_key = f"task_{todo['id']}"
        due_key = f"due_{todo['id']}"
        if task_key not in st.session_state:
            st.session_state[task_key] = todo['task']
        if due_key not in st.session_state and todo['due_date']:
            st.session_state[due_key] = datetime.strptime(todo['due_date'], "%Y-%m-%d").date()
    
    # Add new todo
    with st.form("todo_form"):
        task = st.text_input("New task", label_visibility="collapsed", placeholder="Enter new task...")
        due_date = st.date_input("Due date", min_value=date.today(), label_visibility="collapsed")
        submit = st.form_submit_button("Add Task")
        if submit and task:
            add_todo(task, due_date)
            st.rerun()
    
    # Display todos
    if not todos:
        st.info("No tasks found. Add one above!")
        return
    
    for todo in todos:
        cols = st.columns([0.1, 2, 1.5, 0.5, 0.5])
        with cols[0]:
            completed = st.checkbox(
                "",
                value=todo['completed'],
                key=f"done_{todo['id']}",
                label_visibility="collapsed"
            )
            if completed != todo['completed']:
                update_todo(todo['id'], completed=completed)
                st.rerun()
        
        with cols[1]:
            new_task = st.text_input(
                "Task",
                value=st.session_state[f"task_{todo['id']}"],
                key=f"task_input_{todo['id']}",
                label_visibility="collapsed"
            )
            if new_task != todo['task']:
                update_todo(todo['id'], task=new_task)
                st.rerun()
        
        with cols[2]:
            new_due = st.date_input(
                "Due date",
                value=st.session_state.get(f"due_{todo['id']}", date.today()),
                key=f"due_input_{todo['id']}",
                label_visibility="collapsed"
            )
            if new_due.strftime("%Y-%m-%d") != todo['due_date']:
                update_todo(todo['id'], due_date=new_due.strftime("%Y-%m-%d"))
                st.rerun()
        
        with cols[3]:
            if st.button("🗑️", key=f"del_{todo['id']}"):
                remove_todo(todo['id'])
                st.rerun()
def main():
    st.title("Tools Suite")
    
    # Navigation
    tab1, tab2 = st.tabs(["Network Scanner", "To-Do List"])
    
    with tab1:
        st.header("🔍 Network Scanner")
        with st.form("network_form"):
            network = st.text_input("Network", value="192.168.1.0")
            netmask = st.text_input("Netmask", value="24")
            scan_btn = st.form_submit_button("Start Scan")
        
        if scan_btn:
            with st.spinner(f"Scanning {network}/{netmask}..."):
                live_hosts = ping_sweep(network, netmask)
                if live_hosts:
                    st.success(f"Found {len(live_hosts)} live hosts!")
                    st.json(live_hosts)
                else:
                    st.warning("No live hosts found")
    
    with tab2:
        todo_app()

if __name__ == "__main__":
    main()
