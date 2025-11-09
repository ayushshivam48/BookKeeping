import streamlit as st
import datetime
from decimal import Decimal
import pandas as pd
import pickle

# --- THIS IMPORT IS NOW CORRECTED ---
from ledger_classes import *
# ------------------------------------

# Define a path to save your ledger
LEDGER_FILE = "ledger.pkl"

# --- ALL CLASS DEFINITIONS ARE IN ledger_classes.py ---


# --- 5. Streamlit App Code ---

def initialize_ledger():
    ledger = Ledger()
    # Assets
    ledger.add_account(1001, "Cash", AccountType.ASSET)
    ledger.add_account(1201, "Accounts Receivable", AccountType.ASSET)
    ledger.add_account(1501, "Equipment", AccountType.ASSET)
    # Liabilities
    ledger.add_account(2001, "Accounts Payable", AccountType.LIABILITY)
    ledger.add_account(2101, "Bank Loan", AccountType.LIABILITY)
    # Equity
    ledger.add_account(3001, "Owner's Capital", AccountType.EQUITY)
    # Revenue
    ledger.add_account(4001, "Consulting Revenue", AccountType.REVENUE)
    ledger.add_account(4002, "Product Sales", AccountType.REVENUE)
    # Expenses
    ledger.add_account(5001, "Rent Expense", AccountType.EXPENSE)
    ledger.add_account(5002, "Office Supplies", AccountType.EXPENSE)
    ledger.add_account(5101, "Advertising Expense", AccountType.EXPENSE)
    return ledger

# --- HELPER FUNCTIONS ---
def save_ledger(ledger: Ledger, filepath: str = LEDGER_FILE):
    """Saves the ledger object to a file."""
    with open(filepath, 'wb') as f:
        pickle.dump(ledger, f)

def load_ledger(filepath: str = LEDGER_FILE) -> Ledger:
    """Loads the ledger object from a file, or returns a new one."""
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.info("No saved ledger found. Initializing a new one.")
        return initialize_ledger()
    except Exception as e:
        st.error(f"Error loading ledger: {e}. Initializing a new one.")
        return initialize_ledger()

# --- App Initialization ---
if 'ledger' not in st.session_state:
    st.session_state.ledger = load_ledger()

st.set_page_config(layout="wide")
st.title("📊 Small Business Bookkeeping App")

tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard",
    "✍️ New Journal Entry",
    "🧾 Chart of Accounts",
    "📚 All Entries"
])

# --- Tab 1: Financial Reports ---
with tab1:
    ledger = st.session_state.ledger
    st.header("Financial Dashboard")
    
    total_revenue = Decimal('0.00')
    total_expenses = Decimal('0.00')
    revenue_items = []
    expense_items = []
    zero = Decimal('0.00')

    for acc in ledger.chart_of_accounts.values():
        if acc.account_type == AccountType.REVENUE:
            revenue_amount = -acc.balance
            total_revenue += revenue_amount
            if revenue_amount != zero:
                revenue_items.append({"Account": f"({acc.account_id}) {acc.name}", "Amount": revenue_amount})
        elif acc.account_type == AccountType.EXPENSE:
            total_expenses += acc.balance
            if acc.balance != zero:
                expense_items.append({"Account": f"({acc.account_id}) {acc.name}", "Amount": acc.balance})

    net_income = total_revenue - total_expenses

    total_assets = Decimal('0.00')
    total_liabilities = Decimal('0.00')
    total_equity_base = Decimal('0.00')
    asset_items = []
    liability_items = []
    equity_items = []

    for acc in ledger.chart_of_accounts.values():
        if acc.account_type == AccountType.ASSET:
            total_assets += acc.balance
            if acc.balance != zero:
                asset_items.append({"Account": f"({acc.account_id}) {acc.name}", "Balance": acc.balance})
        elif acc.account_type == AccountType.LIABILITY:
            liability_balance = -acc.balance
            total_liabilities += liability_balance
            if liability_balance != zero:
                liability_items.append({"Account": f"({acc.account_id}) {acc.name}", "Balance": liability_balance})
        elif acc.account_type == AccountType.EQUITY:
            equity_balance = -acc.balance
            total_equity_base += equity_balance
            if equity_balance != zero:
                equity_items.append({"Account": f"({acc.account_id}) {acc.name}", "Balance": equity_balance})

    total_equity = total_equity_base + net_income
    total_liabilities_and_equity = total_liabilities + total_equity

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("Income Statement")
            st.metric(
                label="**Net Income**",
                value=f"${net_income:,.2f}",
                delta=f"${net_income:,.2f}" if net_income != zero else None,
                delta_color="normal" if net_income >= 0 else "inverse"
            )
            if revenue_items:
                st.write("**Revenue**")
                st.dataframe(pd.DataFrame(revenue_items), use_container_width=True, hide_index=True)
            if expense_items:
                st.write("**Expenses**")
                st.dataframe(pd.DataFrame(expense_items), use_container_width=True, hide_index=True)
            st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
            st.metric(label="Total Expenses", value=f"${total_expenses:,.2f}")

    with col2:
        with st.container(border=True):
            st.subheader("Balance Sheet")
            st.metric(label="Total Assets", value=f"${total_assets:,.2f}")
            st.metric(label="Total Liabilities & Equity", value=f"${total_liabilities_and_equity:,.2f}")

            if total_assets.quantize(Decimal('0.01')) == total_liabilities_and_equity.quantize(Decimal('0.01')):
                st.success(f"Balanced: ${total_assets:,.2f} (Assets) = ${total_liabilities_and_equity:,.2f} (Liab + Equity)")
            else:
                st.error(f"Out of balance! Assets: ${total_assets:,.2f} != L+E: ${total_liabilities_and_equity:,.2f}")

            if asset_items:
                st.write("**Assets**")
                st.dataframe(pd.DataFrame(asset_items), use_container_width=True, hide_index=True)
            if liability_items:
                st.write("**Liabilities**")
                st.dataframe(pd.DataFrame(liability_items), use_container_width=True, hide_index=True)
            if equity_items:
                st.write("**Equity**")
                st.dataframe(pd.DataFrame(equity_items), use_container_width=True, hide_index=True)
                st.metric(label="Net Income (retained)", value=f"${net_income:,.2f}")

# --- Tab 2: New Journal Entry ---
with tab2:
    ledger = st.session_state.ledger
    
    account_map = {f"{acc.account_id} - {acc.name}": acc
                   for acc in sorted(ledger.chart_of_accounts.values(), key=lambda x: x.account_id)}
    account_options = list(account_map.keys())
    
    st.header("Post a New Journal Entry")
    st.info("Record a new business transaction. A journal entry must have at least two lines and the total **Debits** must equal the total **Credits**.")

    if 'current_lines' not in st.session_state:
        st.session_state.current_lines = [
            {"Account": None, "Type": "Debit", "Amount": None},
            {"Account": None, "Type": "Credit", "Amount": None},
        ]

    with st.form("new_entry_form"):
        entry_desc = st.text_input("Description", "e.g., Paid monthly rent")
        col1, col2 = st.columns([1,2])
        with col1:
            entry_date = st.date_input("Entry Date", datetime.date.today())
        with col2:
            pass
        st.subheader("Postings (Debits & Credits)")
        with st.container(border=True):
            edited_lines = st.data_editor(
                st.session_state.current_lines,
                num_rows="dynamic",
                column_config={
                    "Account": st.column_config.SelectboxColumn(
                        "Account",
                        options=account_options,
                        required=True
                    ),
                    "Type": st.column_config.SelectboxColumn(
                        "Type",
                        options=["Debit", "Credit"],
                        required=True
                    ),
                    "Amount": st.column_config.NumberColumn(
                        "Amount",
                        format="%.2f",
                        min_value=0.01,
                        required=True
                    )
                },
                use_container_width=True
            )
        st.write("")
        submit_button = st.form_submit_button("Post Journal Entry", type="primary", use_container_width=True)

    # Form submission logic
    if submit_button:
        try:
            new_entry = JournalEntry(date=entry_date, description=entry_desc)
            total_debits = Decimal('0.00')
            total_credits = Decimal('0.00')
            if not edited_lines:
                st.error("Entry must have at least one posting.")
                st.stop()
            valid_lines = 0
            for line in edited_lines:
                if not line["Account"] and not line["Type"] and (line["Amount"] == 0.0 or line["Amount"] is None):
                    continue
                if not line["Account"] or not line["Type"] or (line["Amount"] == 0.0 or line["Amount"] is None):
                    st.error(f"Incomplete line detected. Please fill all fields or remove the line.")
                    st.stop()
                account_obj = account_map[line["Account"]]
                amount = Decimal(str(line["Amount"]))
                is_debit = (line["Type"] == "Debit")
                new_entry.add_posting(account_obj, amount, is_debit)
                valid_lines += 1
                if is_debit:
                    total_debits += amount
                else:
                    total_credits += amount
            if valid_lines < 2:
                st.error("A valid entry must have at least two postings (one debit, one credit).")
                st.stop()
            if not new_entry.validate():
                st.error(f"Entry is not balanced! Debits: {total_debits:,.2f}, Credits: {total_credits:,.2f}")
                st.stop()
            else:
                success = st.session_state.ledger.add_journal_entry(new_entry)

                if success:
                    save_ledger(st.session_state.ledger)
                    st.toast(f"Successfully posted entry: {entry_desc}", icon="✅")
                    st.session_state.current_lines = [
                        {"Account": None, "Type": "Debit", "Amount": None},
                        {"Account": None, "Type": "Credit", "Amount": None},
                    ]
                    st.rerun()
                else:
                    st.error("Entry was valid but failed to post.")
        except Exception as e:
            st.error(f"Failed to post entry: {e}")

# --- Tab 3: Chart of Accounts ---
with tab3:
    ledger = st.session_state.ledger
    st.header("Chart of Accounts")
    st.info("This is a complete list of all accounts (categories) for your business.")

    coa_data = []
    for acc in sorted(ledger.chart_of_accounts.values(), key=lambda x: x.account_id):
        display_balance = acc.balance
        balance_type = acc.account_type.get_balance_type()
        if balance_type == 'credit':
            display_balance = -acc.balance
        coa_data.append({
            "ID": acc.account_id,
            "Name": acc.name,
            "Type": acc.account_type.value,
            "Balance Type": "Debit" if balance_type == 'debit' else "Credit",
            "Balance": f"{display_balance:,.2f}"
        })

    st.dataframe(pd.DataFrame(coa_data), use_container_width=True, hide_index=True)

# --- Tab 4: All Journal Entries ---
with tab4:
    ledger = st.session_state.ledger
    st.header("Journal Entry Log")
    st.info("This is a complete, un-editable history of all transactions posted to the ledger.")
    st.write(f"Total Entries Posted: {len(ledger.journal_entries)}")

    for i, entry in enumerate(reversed(ledger.journal_entries)):
        with st.expander(f"**{entry.date}:** {entry.description} (Entry #{len(ledger.journal_entries) - i})"):
            post_data = []
            for post in entry.postings:
                post_data.append({
                    "Account": f"({post.account.account_id}) {post.account.name}",
                    "Debit": f"{post.amount:,.2f}" if post.is_debit else "",
                    "Credit": f"{post.amount:,.2f}" if not post.is_debit else ""
                })
            st.dataframe(pd.DataFrame(post_data), use_container_width=True, hide_index=True)