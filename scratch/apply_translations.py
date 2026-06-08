import sys
import os

# Reconfigure stdout to use utf-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def apply_translations():
    file_path = "frontend/src/App.jsx"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Define translations dictionary
    translations_code = """const UI_TRANSLATIONS = {
  EN: {
    brandName: "RentalPro Builder",
    dashboard: "Dashboard",
    templates: "Legal Templates",
    conditions: "Manage Conditions",
    tenants: "Tenants & Verification",
    owners: "Owners Registry",
    assets: "Property Assets",
    analytics: "Analytics & Revenue",
    settings: "App Settings",
    print: "Test Print Comparison",
    signOut: "Sign Out",
    newRentalAgreement: "New Rental Agreement",
    dashboardHeader: "Rental Agreement Builder Pro",
    dashboardSub: "Real-time agreement operations console.",
    agreements: "Agreements",
    cloudSecured: "100% cloud secured legal docs",
    activeTenants: "Active Tenants",
    liveRelationships: "Live tenant relationships active",
    expiring30d: "Expiring (30D)",
    requiresRenewal: "Requires renewal action",
    monthlyRevenue: "Monthly Revenue",
    autoTracked: "Auto-tracked through payment sheets",
    monthlyRentInflow: "Monthly Rent Inflow (Consolidated)",
    year2026: "Year 2026",
    operationsJournal: "Operations Journal",
    manageVerifications: "Manage Tenant Verifications",
    portfolio: "Agreements Portfolio",
    all: "All",
    active: "Active",
    expiring: "Expiring",
    draft: "Draft",
    searchAgreements: "Search agreements...",
    verifyApproved: "Verification Approved",
    systemReady: "System Ready",
    aadharVerified: "Aadhar credentials for tenant verified successfully.",
    welcomeBack: "Welcome to RentalPro",
    welcomeSub: "Log in to manage and generate legal document templates.",
    emailAddress: "Email Address",
    password: "Password",
    login: "Log In",
    createAccount: "Create an Account",
    signUp: "Sign Up",
    fullName: "Full Name",
    alreadyHaveAccount: "Already have an account?",
    dontHaveAccount: "Don't have an account?",
    customizeDetails: "Customize Details",
    customizeSub: "Edit contract data below. Your draft preview on the right will update in real-time.",
    leaseConditions: "Lease Conditions",
    manageLeaseConditions: "Manage Lease Conditions",
    quickAddClause: "Quick Add Custom Clause",
    add: "Add",
    hidePanel: "Hide Conditions Panel",
    saveGenerate: "Save & Generate PDF",
    printBtn: "Print",
    downloadDocx: "Download DOCX",
    downloadPdf: "Download PDF",
    docPreview: "Document Preview",
    previewSub: "Toggle views to review draft or inspect PDF print layout.",
    draftText: "Draft Text",
    pdfView: "PDF View",
    nameYourDoc: "Name Your Document",
    nameDocSub: "Please enter a title/filename for this rental agreement. The generated PDF and DOCX files will be saved under this name.",
    docTitleLabel: "Document Title / Filename",
    cancel: "Cancel",
    generateSave: "Generate & Save",
    masterClauseHeader: "Master Clause Registry",
    masterClauseSub: "Manage global template clauses. Changes saved here will be available for all new agreements.",
    createNewMaster: "Create New Master Clause",
    addGlobalClause: "Add Global Clause",
    masterClausePlaceholder: "Type your new clause text here... You can use placeholders like {{RENT_AMOUNT}} or {{LEASE_PERIOD}}.",
    sidebarHeader: "Lease Conditions",
    sidebarSub: "Toggle and edit lease agreement clauses.",
    searchClauses: "Search clauses...",
    createCustomClause: "Create Custom Condition",
    addGlobally: "Add globally",
    addPoint: "Add Point",
    resetDefaults: "Reset to defaults",
    templatesSub: "Select a verified legal template to customize and generate documents.",
    commercialRentalAgreement: "Commercial Rental Agreement",
    commercialRentalSub: "Standard commercial shop lease format containing standard clauses for rent, security deposit, escalation, and signatures.",
    customizeGenerate: "Customize & Generate"
  },
  KN: {
    brandName: "ರೆಂಟಲ್ ಪ್ರೊ ಬಿಲ್ಡರ್",
    dashboard: "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
    templates: "ಕಾನೂನು ಟೆಂಪ್ಲೇಟ್‌ಗಳು",
    conditions: "ಷರತ್ತುಗಳ ನಿರ್ವಹಣೆ",
    tenants: "ಬಾಡಿಗೆದಾರರು & ಪರಿಶೀಲನೆ",
    owners: "ಮಾಲೀಕರ ನೋಂದಣಿ",
    assets: "ಆಸ್ತಿ ವಿವರಗಳು",
    analytics: "ವಿಶ್ಲೇಷಣೆ & ಆದಾಯ",
    settings: "ಅಪ್ಲಿಕೇಶನ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
    print: "ಪ್ರಿಂಟ್ ಹೋಲಿಕೆ ಪರೀಕ್ಷೆ",
    signOut: "ಸೈನ್ ಔಟ್",
    newRentalAgreement: "ಹೊಸ ಬಾಡಿಗೆ ಒಪ್ಪಂದ",
    dashboardHeader: "ಬಾಡಿಗೆ ಒಪ್ಪಂದ ಬಿಲ್ಡರ್ ಪ್ರೊ",
    dashboardSub: "ನೈಜ-ಸಮಯದ ಒಪ್ಪಂದ ಕಾರ್ಯಾಚರಣೆಗಳ ನಿಯಂತ್ರಣ.",
    agreements: "ಒಪ್ಪಂದಗಳು",
    cloudSecured: "100% ಕ್ಲೌಡ್ ಸುರಕ್ಷಿತ ಕಾನೂನು ದಾಖಲೆಗಳು",
    activeTenants: "ಸಕ್ರಿಯ ಬಾಡಿಗೆದಾರರು",
    liveRelationships: "ಬಾಡಿಗೆದಾರರ ಸಕ್ರಿಯ ಸಂಪರ್ಕಗಳು",
    expiring30d: "ಅವಧಿ ಮುಗಿಯುವ ಹಂತದಲ್ಲಿರುವ (30 ದಿನಗಳು)",
    requiresRenewal: "ನವೀಕರಣದ ಅಗತ್ಯವಿದೆ",
    monthlyRevenue: "ಮಾಸಿಕ ಆದಾಯ",
    autoTracked: "ಪಾವತಿ ದಾಖಲೆಗಳಿಂದ ಸ್ವಯಂಚಾಲಿತ ಟ್ರ್ಯಾಕ್",
    monthlyRentInflow: "ಮಾಸಿಕ ಬಾಡಿಗೆ ಒಳಹರಿವು (ಕ್ರೋಢೀಕರಿಸಿದ)",
    year2026: "ವರ್ಷ 2026",
    operationsJournal: "ಕಾರ್ಯಾಚರಣೆ ದಿನಚರಿ",
    manageVerifications: "ಬಾಡಿಗೆದಾರರ ಪರಿಶೀಲನೆ ನಿರ್ವಹಿಸಿ",
    portfolio: "ಒಪ್ಪಂದಗಳ ಬಂಡವಾಳ",
    all: "ಎಲ್ಲಾ",
    active: "ಸಕ್ರಿಯ",
    expiring: "ಅವಧಿ ಮುಗಿಯುವ",
    draft: "ಕರಡು",
    searchAgreements: "ಒಪ್ಪಂದಗಳನ್ನು ಹುಡುಕಿ...",
    verifyApproved: "ಪರಿಶೀಲನೆ ಅನುಮೋದಿಸಲಾಗಿದೆ",
    systemReady: "ಸಿಸ್ಟಮ್ ಸಿದ್ಧವಾಗಿದೆ",
    aadharVerified: "ಬಾಡಿಗೆದಾರರ ಆಧಾರ್ ವಿವರಗಳು ಯಶಸ್ವಿಯಾಗಿ ಪರಿಶೀಲಿಸಲ್ಪಟ್ಟಿವೆ.",
    welcomeBack: "ರೆಂಟಲ್ ಪ್ರೊಗೆ ಸ್ವಾಗತ",
    welcomeSub: "ಕಾನೂನು ದಾಖಲೆಗಳ ಟೆಂಪ್ಲೇಟ್‌ಗಳನ್ನು ನಿರ್ವಹಿಸಲು ಮತ್ತು ರಚಿಸಲು ಲಾಗ್ ಇನ್ ಮಾಡಿ.",
    emailAddress: "ಇಮೇಲ್ ವಿಳಾಸ",
    password: "ಪಾಸ್ವರ್ಡ್",
    login: "ಲಾಗ್ ಇನ್",
    createAccount: "ಖಾತೆ ರಚಿಸಿ",
    signUp: "ಸೈನ್ ಅಪ್",
    fullName: "ಪೂರ್ಣ ಹೆಸರು",
    alreadyHaveAccount: "ಈಗಾಗಲೇ ಖಾತೆ ಹೊಂದಿದ್ದೀರಾ?",
    dontHaveAccount: "ಖಾತೆ ಹೊಂದಿಲ್ಲವೇ?",
    customizeDetails: "ವಿವರಗಳನ್ನು ಕಸ್ಟಮೈಸ್ ಮಾಡಿ",
    customizeSub: "ಕೆಳಗಿನ ಒಪ್ಪಂದದ ಡೇಟಾವನ್ನು ಸಂಪಾದಿಸಿ. ಬಲಭಾಗದಲ್ಲಿರುವ ಕರಡು ಮುನ್ನೋಟವು ನೈಜ ಸಮಯದಲ್ಲಿ ನವೀಕರಣಗೊಳ್ಳುತ್ತದೆ.",
    leaseConditions: "ಬಾಡಿಗೆ ಷರತ್ತುಗಳು",
    manageLeaseConditions: "ಬಾಡಿಗೆ ಷರತ್ತುಗಳನ್ನು ನಿರ್ವಹಿಸಿ",
    quickAddClause: "ಕಸ್ಟಮ್ ಷರತ್ತನ್ನು ತ್ವರಿತವಾಗಿ ಸೇರಿಸಿ",
    add: "ಸೇರಿಸಿ",
    hidePanel: "ಷರತ್ತುಗಳ ಫಲಕವನ್ನು ಮರೆಮಾಡಿ",
    saveGenerate: "ಉಳಿಸಿ & PDF ರಚಿಸಿ",
    printBtn: "ಪ್ರಿಂಟ್",
    downloadDocx: "DOCX ಡೌನ್‌ಲೋಡ್",
    downloadPdf: "PDF ಡೌನ್‌ಲೋಡ್",
    docPreview: "ದಾಖಲೆ ಮುನ್ನೋಟ",
    previewSub: "ಕರಡು ಪರಿಶೀಲಿಸಲು ಅಥವಾ PDF ಪ್ರಿಂಟ್ ವಿನ್ಯಾಸವನ್ನು ವೀಕ್ಷಿಸಲು ಬದಲಿಸಿ.",
    draftText: "ಕರಡು ಪಠ್ಯ",
    pdfView: "PDF ಮುನ್ನೋಟ",
    nameYourDoc: "ನಿಮ್ಮ ದಾಖಲೆಗೆ ಹೆಸರಿಸಿ",
    nameDocSub: "ದಯವಿಟ್ಟು ಈ ಬಾಡಿಗೆ ಒಪ್ಪಂದಕ್ಕೆ ಶೀರ್ಷಿಕೆ/ಫೈಲ್ ಹೆಸರನ್ನು ನಮೂದಿಸಿ. ರಚಿಸಲಾದ PDF ಮತ್ತು DOCX ಫೈಲ್‌ಗಳನ್ನು ಈ ಹೆಸರಿನಲ್ಲಿ ಉಳಿಸಲಾಗುತ್ತದೆ.",
    docTitleLabel: "ದಾಖಲೆಯ ಶೀರ್ಷಿಕೆ / ಫೈಲ್ ಹೆಸರು",
    cancel: "ರದ್ದುಮಾಡಿ",
    generateSave: "ರಚಿಸಿ & ಉಳಿಸಿ",
    masterClauseHeader: "ಮುಖ್ಯ ಷರತ್ತುಗಳ ನೋಂದಣಿ",
    masterClauseSub: "ಜಾಗತಿಕ ಟೆಂಪ್ಲೇಟ್ ಷರತ್ತುಗಳನ್ನು ನಿರ್ವಹಿಸಿ. ಇಲ್ಲಿ ಉಳಿಸಲಾದ ಬದಲಾವಣೆಗಳು ಎಲ್ಲಾ ಹೊಸ ಒಪ್ಪಂದಗಳಿಗೆ ಲಭ್ಯವಿರುತ್ತವೆ.",
    createNewMaster: "ಹೊಸ ಮುಖ್ಯ ಷರತ್ತನ್ನು ರಚಿಸಿ",
    addGlobalClause: "ಜಾಗತಿಕ ಷರತ್ತು ಸೇರಿಸಿ",
    masterClausePlaceholder: "ನಿಮ್ಮ ಹೊಸ ಷರತ್ತಿನ ಪಠ್ಯವನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ... ನೀವು {{RENT_AMOUNT}} ಅಥವಾ {{LEASE_PERIOD}} ನಂತಹ ಪ್ಲೇಸ್‌ಹೋಲ್ಡರ್‌ಗಳನ್ನು ಬಳಸಬಹುದು.",
    sidebarHeader: "ಬಾಡಿಗೆ ಷರತ್ತುಗಳು",
    sidebarSub: "ಬಾಡಿಗೆ ಒಪ್ಪಂದದ ಷರತ್ತುಗಳನ್ನು ಬದಲಿಸಿ ಮತ್ತು ಸಂಪಾದಿಸಿ.",
    searchClauses: "ಷರತ್ತುಗಳನ್ನು ಹುಡುಕಿ...",
    createCustomClause: "ಕಸ್ಟಮ್ ಷರತ್ತು ರಚಿಸಿ",
    addGlobally: "ಜಾಗತಿಕವಾಗಿ ಸೇರಿಸಿ",
    addPoint: "ಅಂಶವನ್ನು ಸೇರಿಸಿ",
    resetDefaults: "ಡೀಫಾಲ್ಟ್‌ಗಳಿಗೆ ಮರುಹೊಂದಿಸಿ",
    templatesSub: "ಕಸ್ಟಮೈಸ್ ಮಾಡಲು ಮತ್ತು ದಾಖಲೆಗಳನ್ನು ರಚಿಸಲು ಪರಿಶೀಲಿಸಿದ ಕಾನೂನು ಟೆಂಪ್ಲೇಟ್ ಅನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
    commercialRentalAgreement: "ವಾಣಿಜ್ಯ ಬಾಡಿಗೆ ಒಪ್ಪಂದ",
    commercialRentalSub: "ಬಾಡಿಗೆ, ಭದ್ರತಾ ಠೇವಣಿ, ಹೆಚ್ಚಳ ಮತ್ತು ಸಹಿಗಳಿಗಾಗಿ ಪ್ರಮಾಣಿತ ಷರತ್ತುಗಳನ್ನು ಒಳಗೊಂಡಿರುವ ಪ್ರಮಾಣಿತ ವಾಣಿಜ್ಯ ಅಂಗಡಿ ಬಾಡಿಗೆ ಸ್ವರೂಪ.",
    customizeGenerate: "ಕಸ್ಟಮೈಸ್ & ಜನರೇಟ್"
  }
};
"""

    # Replace export default function App() { with translations + helper t
    old_def = "export default function App() {"
    new_def = f"{translations_code}\n\nexport default function App() {{\n  const [language, setLanguage] = sys_useState_placeholder;\n  const t = (key) => UI_TRANSLATIONS[language]?.[key] || UI_TRANSLATIONS.EN[key];"

    # We need to find the correct useState for language.
    # Currently: const [language, setLanguage] = useState("EN");
    # We will remove the old useState("EN") and replace the export default function App()
    
    # 2. Update state declarations
    content = content.replace('const [language, setLanguage] = useState("EN");', '')
    
    # In the App function definition, inject language from localstorage, with an effect
    new_def_real = f"""{translations_code}

export default function App() {{
  const [language, setLanguage] = useState(() => localStorage.getItem("language") || "EN");
  const t = (key) => UI_TRANSLATIONS[language]?.[key] || UI_TRANSLATIONS.EN[key];

  useEffect(() => {{
    localStorage.setItem("language", language);
  }}, [language]);"""

    content = content.replace("export default function App() {", new_def_real)

    # 3. Translate Sidebar items label
    # Old: { id: "dashboard", label: "Dashboard", icon: () => <SlidersHorizontal className="w-4 h-4" /> },
    # Replace label property:
    content = content.replace('label: "Dashboard"', 'label: t("dashboard")')
    content = content.replace('label: "Legal Templates"', 'label: t("templates")')
    content = content.replace('label: "Manage Conditions"', 'label: t("conditions")')
    content = content.replace('label: "Tenants & Verification"', 'label: t("tenants")')
    content = content.replace('label: "Owners Registry"', 'label: t("owners")')
    content = content.replace('label: "Property Assets"', 'label: t("assets")')
    content = content.replace('label: "Analytics & Revenue"', 'label: t("analytics")')
    content = content.replace('label: "App Settings"', 'label: t("settings")')
    content = content.replace('label: "Test Print Comparison"', 'label: t("print")')
    content = content.replace('{item.label}', '{t(item.id)}')

    # 4. Brand Name
    content = content.replace('RentalPro Builder\n', '{t("brandName")}\n')
    content = content.replace('RentalPro Builder<', '{t("brandName")}<')

    # 5. Sign Out
    content = content.replace('Sign Out', '{t("signOut")}')

    # 6. New Rental Agreement
    content = content.replace('New Rental Agreement', '{t("newRentalAgreement")}')

    # 7. Dashboard header & sub
    content = content.replace('Rental Agreement Builder Pro', '{t("dashboardHeader")}')
    content = content.replace('Real-time agreement operations console.', '{t("dashboardSub")}')

    # 8. Indicators metrics
    content = content.replace('text-slate-400 uppercase tracking-wider">\n                          Agreements\n', 'text-slate-400 uppercase tracking-wider">\n                          {t("agreements")}\n')
    content = content.replace('100% cloud secured legal docs', '{t("cloudSecured")}')
    content = content.replace('Active Tenants', '{t("activeTenants")}')
    content = content.replace('Live tenant relationships active', '{t("liveRelationships")}')
    content = content.replace('Expiring (30D)', '{t("expiring30d")}')
    content = content.replace('Requires renewal action', '{t("requiresRenewal")}')
    content = content.replace('Monthly Revenue', '{t("monthlyRevenue")}')
    content = content.replace('Auto-tracked through payment sheets', '{t("autoTracked")}')

    # 9. Inflow
    content = content.replace('Monthly Rent Inflow (Consolidated)', '{t("monthlyRentInflow")}')
    content = content.replace('Year 2026', '{t("year2026")}')

    # 10. Operations Journal & verification
    content = content.replace('Operations Journal', '{t("operationsJournal")}')
    content = content.replace('Manage Tenant Verifications', '{t("manageVerifications")}')

    # 11. Portfolio
    content = content.replace('Agreements Portfolio', '{t("portfolio")}')
    content = content.replace('label: "All"', 'label: t("all")')
    content = content.replace('label: "Active"', 'label: t("active")')
    content = content.replace('label: "Expiring"', 'label: t("expiring")')
    content = content.replace('label: "Draft"', 'label: t("draft")')
    content = content.replace('{tab.label}', '{t(tab.id)}')
    content = content.replace('placeholder="Search agreements..."', 'placeholder={t("searchAgreements")}')

    # 12. Language toggle button
    old_lang_toggle = """                {/* Language Pill */}
                <button
                  onClick={() => {
                    const nextLang = language === "EN" ? "HI" : "EN";
                    setLanguage(nextLang);
                    showToast(`Language switched to ${nextLang === "EN" ? "English" : "Hindi (हिंदी)"}`, "success");
                  }}
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200/60 shadow-sm hover:border-slate-300 dark:bg-slate-900/40 dark:border-slate-800 text-xs font-bold text-slate-600 hover:text-slate-800 dark:text-slate-350 dark:hover:text-white active:scale-95 transition-all cursor-pointer"
                >
                  <Globe className="w-3.5 h-3.5 text-slate-400" />
                  <span>{language}</span>
                </button>"""

    new_lang_toggle = """                {/* Language Pill */}
                <button
                  onClick={() => {
                    const nextLang = language === "EN" ? "KN" : "EN";
                    setLanguage(nextLang);
                    showToast(`Language switched to ${nextLang === "EN" ? "English" : "Kannada (ಕನ್ನಡ)"}`, "success");
                  }}
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200/60 shadow-sm hover:border-slate-300 dark:bg-slate-900/40 dark:border-slate-800 text-xs font-bold text-slate-600 hover:text-slate-800 dark:text-slate-350 dark:hover:text-white active:scale-95 transition-all cursor-pointer"
                >
                  <Globe className="w-3.5 h-3.5 text-slate-400" />
                  <span>{language === "EN" ? "EN" : "KN"}</span>
                </button>"""
    
    content = content.replace(old_lang_toggle, new_lang_toggle)

    # 13. Login / Register
    content = content.replace('Welcome to RentalPro', '{t("welcomeBack")}')
    content = content.replace('Log in to manage and generate legal document templates.', '{t("welcomeSub")}')
    content = content.replace('Email Address', '{t("emailAddress")}')
    content = content.replace('Password', '{t("password")}')
    content = content.replace('>Log In<', '>{t("login")}<')
    content = content.replace('Create an Account', '{t("createAccount")}')
    content = content.replace('Sign Up', '{t("signUp")}')
    content = content.replace('Full Name', '{t("fullName")}')
    content = content.replace("Already have an account?", '{t("alreadyHaveAccount")}')
    content = content.replace("Don't have an account?", '{t("dontHaveAccount")}')

    # 14. Editor details Customize
    content = content.replace('Customize Details', '{t("customizeDetails")}')
    content = content.replace('Edit contract data below. Your draft preview on the right will update in real-time.', '{t("customizeSub")}')
    content = content.replace('Lease Conditions', '{t("leaseConditions")}')
    content = content.replace('Manage Lease Conditions', '{t("manageLeaseConditions")}')
    content = content.replace('Quick Add Custom Clause', '{t("quickAddClause")}')
    content = content.replace('>Add<', '>{t("add")}<')
    content = content.replace('Hide Conditions Panel', '{t("hidePanel")}')
    content = content.replace('Save & Generate PDF', '{t("saveGenerate")}')
    content = content.replace('>Print<', '>{t("printBtn")}<')
    content = content.replace('Download DOCX', '{t("downloadDocx")}')
    content = content.replace('Download PDF', '{t("downloadPdf")}')
    
    # 15. Preview
    content = content.replace('Document Preview', '{t("docPreview")}')
    content = content.replace('Toggle views to review draft or inspect PDF print layout.', '{t("previewSub")}')
    content = content.replace('Draft Text', '{t("draftText")}')
    content = content.replace('PDF View', '{t("pdfView")}')

    # 16. Modal
    content = content.replace('Name Your Document', '{t("nameYourDoc")}')
    content = content.replace('Please enter a title/filename for this rental agreement. The generated PDF and DOCX files will be saved under this name.', '{t("nameDocSub")}')
    content = content.replace('Document Title / Filename', '{t("docTitleLabel")}')
    content = content.replace('>Cancel<', '>{t("cancel")}<')
    content = content.replace('Generate & Save', '{t("generateSave")}')

    # 17. Master Clause
    content = content.replace('Master Clause Registry', '{t("masterClauseHeader")}')
    content = content.replace('Manage global template clauses. Changes saved here will be available for all new agreements.', '{t("masterClauseSub")}')
    content = content.replace('Create New Master Clause', '{t("createNewMaster")}')
    content = content.replace('Add Global Clause', '{t("addGlobalClause")}')
    content = content.replace('placeholder="Type your new clause text here... You can use placeholders like {{RENT_AMOUNT}} or {{LEASE_PERIOD}}."', 'placeholder={t("masterClausePlaceholder")}')

    # 18. Sidebar Conditions
    content = content.replace('Toggle and edit lease agreement clauses.', '{t("sidebarSub")}')
    content = content.replace('placeholder="Search clauses..."', 'placeholder={t("searchClauses")}')
    content = content.replace('Create Custom Condition', '{t("createCustomClause")}')
    content = content.replace('Add globally', '{t("addGlobally")}')
    content = content.replace('Add Point', '{t("addPoint")}')
    content = content.replace('Reset to defaults', '{t("resetDefaults")}')

    # 19. Templates tab
    content = content.replace('Legal Document Templates', '{t("legalTemplates")}')
    content = content.replace('Select a verified legal template to customize and generate documents.', '{t("templatesSub")}')
    content = content.replace('Commercial Rental Agreement', '{t("commercialRentalAgreement")}')
    content = content.replace('Standard commercial shop lease format containing standard clauses for rent, security deposit, escalation, and signatures.', '{t("commercialRentalSub")}')
    content = content.replace('Customize & Generate', '{t("customizeGenerate")}')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Translations applied successfully to App.jsx.")

if __name__ == "__main__":
    apply_translations()
