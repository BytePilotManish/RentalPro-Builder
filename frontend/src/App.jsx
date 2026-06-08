import { useState, useEffect, useRef } from "react";
import { 
  FileSignature, 
  Moon, 
  Sun, 
  SlidersHorizontal, 
  Eye, 
  FileText, 
  Printer, 
  FileDown, 
  Loader2, 
  CheckCircle2, 
  AlertCircle,
  FileSpreadsheet,
  Plus,
  Trash2,
  Edit2,
  LogOut,
  User as UserIcon,
  Search,
  ArrowLeft,
  Lock,
  Mail,
  UserPlus,
  Globe,
  Bell,
  Sparkles,
  Users,
  IndianRupee,
  AlertTriangle,
  Building,
  TrendingUp,
  Settings,
  Folder,
  Layers,
  Maximize2
} from "lucide-react";

// Number to words conversion (Indian Numbering System)
const numberToWords = (numStr) => {
  const clean = numStr.replace(/,/g, "").trim();
  const num = parseInt(clean, 10);
  if (isNaN(num) || num === 0) return "";

  const ones = [
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
    "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"
  ];
  const tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"];

  const convertLessThanThousand = (n) => {
    let str = "";
    if (n >= 100) {
      str += ones[Math.floor(n / 100)] + " Hundred ";
      n %= 100;
    }
    if (n >= 20) {
      str += tens[Math.floor(n / 10)] + " ";
      n %= 10;
    }
    if (n > 0) {
      str += ones[n] + " ";
    }
    return str.trim();
  };

  let temp = num;
  let str = "";

  if (temp >= 10000000) {
    str += convertLessThanThousand(Math.floor(temp / 10000000)) + " Crore ";
    temp %= 10000000;
  }
  if (temp >= 100000) {
    str += convertLessThanThousand(Math.floor(temp / 100000)) + " Lakh ";
    temp %= 100000;
  }
  if (temp >= 1000) {
    str += convertLessThanThousand(Math.floor(temp / 1000)) + " Thousand ";
    temp %= 1000;
  }
  if (temp > 0) {
    str += convertLessThanThousand(temp);
  }

  return str.trim();
};

const DEFAULT_CONDITIONS = [
  "This RENTAL AGREEMENT is for a period of {{LEASE_PERIOD}} from the date of execution of this agreement i.e., on {{LEASE_END_DATE}}.",
  "The OWNER has agreed to let out the said premises for a monthly rent of Rs.{{RENT_AMOUNT}} (Rupees {{RENT_AMOUNT_WORDS}} only)",
  "The TENANT has agreed to pay the rental amount on {{RENT_PAYMENT_DAY}} of every month.",
  "The TENANT has agreed to pay {{ESCALATION_RATE}} increase in the rent every {{LEASE_PERIOD_NUM}} months, over the previous monthly rent.",
  "The TENANT has paid Security deposited to the OWNER an amount of Rs {{DEPOSIT_AMOUNT}}/- (Rupees {{DEPOSIT_AMOUNT_WORDS}} only) by way of {{DEPOSIT_MODE}} as an advance deposit amount. The OWNER has agreed to refund the said amount without interest to the TENANT while vacating the rented premises. The TENANT has agreed for the same. The OWNER hereby acknowledges the receipt of the said amount from the tenant.",
  "The TENANT should use the rented premises for his Business Purpose Only, and not for any illegal trade or business and unlawful purpose like to endanger the building.",
  "The TENANT should pay the Electricity and water charges utilized for his own use as per the actual meter reading for the rented premises during the period of tenancy.",
  "The tenancy period may be renewed for further period of {{LEASE_PERIOD_NUM}} months by mutual agreement between the OWNER and TENANT on the terms and conditions to be specified at that time.",
  "The OWNER and TENANT have agreed that {{NOTICE_PERIOD}} prior notice on either side is required for the termination of the tenancy period."
];

const UI_TRANSLATIONS = {
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


export default function App() {
  const [language, setLanguage] = useState(() => localStorage.getItem("language") || "EN");
  const t = (key) => UI_TRANSLATIONS[language]?.[key] || UI_TRANSLATIONS.EN[key];

  useEffect(() => {
    localStorage.setItem("language", language);
  }, [language]);
  // Theme state: default to "light" for a cleaner, easier to read experience
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "light");
  
  // Master conditions loaded from localStorage or default
  const [masterConditions, setMasterConditions] = useState(() => {
    const saved = localStorage.getItem("master_conditions");
    if (saved) return JSON.parse(saved);
    return DEFAULT_CONDITIONS;
  });
  
  // Agreement-specific conditions state
  const [agreementConditions, setAgreementConditions] = useState([]);
  
  // Navigation & Auth state
  const [currentView, setCurrentView] = useState("login"); // "login", "register", "dashboard", "editor"
  const [authToken, setAuthToken] = useState(() => localStorage.getItem("token") || "");
  const [userProfile, setUserProfile] = useState(null);
  
  // Form fields configuration loaded from API
  const [fieldsConfig, setFieldsConfig] = useState(null);
  
  // Dashboard state
  const [agreements, setAgreements] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDeletingId, setIsDeletingId] = useState(null);
  const [isDataLoading, setIsDataLoading] = useState(false);

  // Editor/Customizer state
  const [editorId, setEditorId] = useState(null); // null if new, number if editing
  const [editorTitle, setEditorTitle] = useState("New Rental Agreement");
  const [formData, setFormData] = useState({});
  const [activePreviewTab, setActivePreviewTab] = useState("draft"); // "draft" or "pdf"
  const [isGenerating, setIsGenerating] = useState(false);
  const [pdfGenerated, setPdfGenerated] = useState(false);
  const [downloadUrls, setDownloadUrls] = useState({ docx: "", pdf: "" });
  const [changedField, setChangedField] = useState(null);
  const [fullscreenMode, setFullscreenMode] = useState("none"); // "none", "split", "document"
  const [showFilenameModal, setShowFilenameModal] = useState(false);
  const [filenameInput, setFilenameInput] = useState("");
  // Admin-only document creation charge (earning for preparing this document)
  const [feeInput, setFeeInput] = useState("");
  const [showConditionsSidebar, setShowConditionsSidebar] = useState(false);
  const [clauseSearchQuery, setClauseSearchQuery] = useState("");

  // Toast notification state
  const [toast, setToast] = useState({ show: false, message: "", type: "info" });
  
  // Login/Register credentials
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [regName, setRegName] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regPassword, setRegPassword] = useState("");

  // Dashboard view options
  const [portfolioFilter, setPortfolioFilter] = useState("all"); // "all", "active", "expiring", "draft"
  const [activeSidebarTab, setActiveSidebarTab] = useState("dashboard"); // "dashboard", "templates", "tenants", "owners", "assets", "analytics", "settings", "print"
  
  const [showNotifications, setShowNotifications] = useState(false);
  const [hasNewNotifications, setHasNewNotifications] = useState(true);

  // Software update state
  const [updateInfo, setUpdateInfo] = useState(null);
  const [checkingUpdate, setCheckingUpdate] = useState(false);
  const [applyingUpdate, setApplyingUpdate] = useState(false);

  // Real-time calculation helpers
  const parseCurrency = (val) => {
    if (!val) return 0;
    const clean = val.toString().replace(/,/g, "").replace(/Rs\.?/gi, "").trim();
    const parsed = parseFloat(clean);
    return isNaN(parsed) ? 0 : parsed;
  };

  const parseLeaseEndDate = (dateStr) => {
    if (!dateStr) return null;
    const parts = dateStr.toString().split("/");
    if (parts.length === 3) {
      const day = parseInt(parts[0], 10);
      const month = parseInt(parts[1], 10) - 1;
      const year = parseInt(parts[2], 10);
      if (!isNaN(day) && !isNaN(month) && !isNaN(year)) {
        return new Date(year, month, day);
      }
    }
    const parsed = new Date(dateStr);
    return isNaN(parsed.getTime()) ? null : parsed;
  };

  const parseLeaseStartDate = (dateStr) => {
    if (!dateStr) return null;
    const str = dateStr.toString().toLowerCase();
    
    // Try to find a year (4 digits)
    const yearMatch = str.match(/\b(20\d{2})\b/);
    const year = yearMatch ? parseInt(yearMatch[1], 10) : 2026;
    
    // Try to find a month name
    const months = [
      "jan", "feb", "mar", "apr", "may", "jun",
      "jul", "aug", "sep", "oct", "nov", "dec"
    ];
    
    for (let i = 0; i < months.length; i++) {
      if (str.includes(months[i])) {
        return new Date(year, i, 1);
      }
    }
    
    // Fallback to DD/MM/YYYY parsing if month name not found
    const parts = str.split("/");
    if (parts.length === 3) {
      const day = parseInt(parts[0], 10);
      const month = parseInt(parts[1], 10) - 1;
      const yearPart = parseInt(parts[2], 10);
      if (!isNaN(day) && !isNaN(month) && !isNaN(yearPart)) {
        return new Date(yearPart, month, 1);
      }
    }
    
    const parsed = new Date(dateStr);
    return isNaN(parsed.getTime()) ? null : new Date(parsed.getFullYear(), parsed.getMonth(), 1);
  };

  const isLeaseActive = (ag) => {
    const endDate = parseLeaseEndDate(ag.data?.LEASE_END_DATE);
    if (!endDate) return true;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return endDate >= today;
  };

  const isLeaseExpiring30D = (ag) => {
    const endDate = parseLeaseEndDate(ag.data?.LEASE_END_DATE);
    if (!endDate) return false;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const diffTime = endDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays >= 0 && diffDays <= 30;
  };

  const renderClauseWithHighlights = (clauseText) => {
    if (!clauseText) return "";
    const regex = /\{\{([A-Z0-9_]+)\}\}/g;
    const parts = [];
    let lastIndex = 0;
    let match;
    while ((match = regex.exec(clauseText)) !== null) {
      const fieldKey = match[1];
      const matchIndex = match.index;
      if (matchIndex > lastIndex) {
        parts.push(clauseText.substring(lastIndex, matchIndex));
      }
      parts.push(renderHighlight(fieldKey));
      lastIndex = regex.lastIndex;
    }
    if (lastIndex < clauseText.length) {
      parts.push(clauseText.substring(lastIndex));
    }
    return <>{parts}</>;
  };

  const iframeRef = useRef(null);

  // Initialize theme class helper
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  // Toast notifier helper
  const showToast = (message, type = "info") => {
    setToast({ show: true, message, type });
    setTimeout(() => {
      setToast(prev => ({ ...prev, show: false }));
    }, 3500);
  };

  const toggleTheme = () => {
    setTheme(prev => (prev === "dark" ? "light" : "dark"));
  };

  const updateMasterConditionsState = async (newConditions) => {
    setMasterConditions(newConditions);
    localStorage.setItem("master_conditions", JSON.stringify(newConditions));
    if (authToken) {
      try {
        await fetch("/api/auth/conditions", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${authToken}`
          },
          body: JSON.stringify({ conditions: newConditions })
        });
      } catch (err) {
        console.error("Failed to sync master conditions to DB:", err);
      }
    }
  };

  // API Calls
  const fetchProfile = async () => {
    try {
      const res = await fetch("/api/auth/me", {
        headers: { "Authorization": `Bearer ${authToken}` }
      });
      if (res.status === 401) {
        handleLogout();
        return;
      }
      if (!res.ok) throw new Error("Failed to fetch profile");
      const data = await res.json();
      setUserProfile(data);
      if (data.master_conditions) {
        setMasterConditions(data.master_conditions);
        localStorage.setItem("master_conditions", JSON.stringify(data.master_conditions));
      }
    } catch (err) {
      showToast(err.message, "error");
    }
  };

  const fetchFieldsConfig = async () => {
    try {
      const res = await fetch("/api/fields");
      if (!res.ok) throw new Error("Failed to fetch template fields");
      const data = await res.json();
      setFieldsConfig(data);
    } catch (err) {
      showToast(err.message, "error");
    }
  };

  const fetchAgreements = async () => {
    setIsDataLoading(true);
    try {
      const res = await fetch("/api/agreements", {
        headers: { "Authorization": `Bearer ${authToken}` }
      });
      if (!res.ok) throw new Error("Failed to fetch agreements list");
      const data = await res.json();
      setAgreements(data);
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setIsDataLoading(false);
    }
  };

  const checkForUpdates = async () => {
    setCheckingUpdate(true);
    try {
      const res = await fetch("/api/update/check", {
        headers: { "Authorization": `Bearer ${authToken}` }
      });
      if (!res.ok) throw new Error("Update check failed");
      const data = await res.json();
      setUpdateInfo(data);
      if (!data.enabled) {
        showToast("Auto-update works only in the installed desktop app.", "info");
      } else if (data.available) {
        showToast(`Update available: v${data.latest}`, "success");
      } else {
        showToast("You're on the latest version.", "success");
      }
    } catch (err) {
      showToast(err.message || "Could not check for updates.", "error");
    } finally {
      setCheckingUpdate(false);
    }
  };

  const applyUpdate = async () => {
    setApplyingUpdate(true);
    try {
      const res = await fetch("/api/update/apply", {
        method: "POST",
        headers: { "Authorization": `Bearer ${authToken}` }
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Update failed to start.");
      }
      showToast("Downloading update… the app will restart automatically.", "success");
    } catch (err) {
      showToast(err.message, "error");
      setApplyingUpdate(false);
    }
  };

  // Actions
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: loginEmail, password: loginPassword })
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Authentication failed.");
      
      setAuthToken(data.token);
      showToast(`Welcome back, ${data.user.full_name}!`, "success");
      setLoginEmail("");
      setLoginPassword("");
    } catch (err) {
      showToast(err.message, "error");
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: regEmail, password: regPassword, full_name: regName })
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Registration failed.");
      
      setAuthToken(data.token);
      showToast("Account registered successfully!", "success");
      setRegName("");
      setRegEmail("");
      setRegPassword("");
    } catch (err) {
      showToast(err.message, "error");
    }
  };

  const handleLogout = () => {
    setAuthToken("");
    setAgreements([]);
    setUserProfile(null);
  };

  // Load profile and config whenever the auth token changes
  useEffect(() => {
    if (authToken) {
      localStorage.setItem("token", authToken);
      // eslint-disable-next-line react-hooks/set-state-in-effect
      fetchProfile();
      fetchFieldsConfig();
      fetchAgreements();
      setCurrentView("dashboard");
    } else {
      localStorage.removeItem("token");
      setUserProfile(null);
      setCurrentView("login");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [authToken]);

  const startNewAgreement = () => {
    setEditorId(null);
    setEditorTitle(t("newRentalAgreement"));
    setActivePreviewTab("draft");
    setPdfGenerated(false);
    
    // Initialize agreementConditions from masterConditions
    const initialConditions = masterConditions.map((masterText, idx) => ({
      id: `master-${idx}-${Date.now()}`,
      text: masterText,
      checked: true
    }));
    setAgreementConditions(initialConditions);
    
    const initialData = {};
    if (fieldsConfig) {
      Object.values(fieldsConfig).forEach(category => {
        Object.entries(category.fields).forEach(([key, field]) => {
          initialData[key] = field.default;
        });
      });
    }
    setFormData(initialData);
    setCurrentView("editor");
  };

  const editAgreement = (agreement) => {
    setEditorId(agreement.id);
    setEditorTitle(agreement.title);
    setFormData(agreement.data);
    setPdfGenerated(true);
    setDownloadUrls({
      docx: `${agreement.docx_url}?token=${authToken}`,
      pdf: `${agreement.pdf_url}?token=${authToken}`
    });
    
    // Populate agreementConditions
    const savedClauses = agreement.data?.AGREEMENT_CONDITIONS || [];
    const localConditions = [];
    
    // First add saved ones
    savedClauses.forEach((clauseText, idx) => {
      localConditions.push({
        id: `saved-${idx}-${Date.now()}`,
        text: clauseText,
        checked: true
      });
    });
    
    // Then add any master ones that are not already in saved ones
    masterConditions.forEach((masterText, idx) => {
      const isAlreadySaved = savedClauses.some(savedText => savedText === masterText);
      if (!isAlreadySaved) {
        localConditions.push({
          id: `master-${idx}-${Date.now()}`,
          text: masterText,
          checked: false
        });
      }
    });
    setAgreementConditions(localConditions);

    setActivePreviewTab("draft");
    setCurrentView("editor");
    
    setTimeout(() => {
      if (iframeRef.current) {
        iframeRef.current.src = `${agreement.pdf_url}?token=${authToken}`;
      }
    }, 100);
  };

  const deleteAgreement = async (id) => {
    if (window.confirm("Are you sure you want to delete this agreement?")) {
      setIsDeletingId(id);
      try {
        const res = await fetch(`/api/agreements/${id}`, {
          method: "DELETE",
          headers: { "Authorization": `Bearer ${authToken}` }
        });
        if (!res.ok) throw new Error("Failed to delete agreement");
        
        showToast("Agreement deleted successfully.", "success");
        setAgreements(prev => prev.filter(ag => ag.id !== id));
      } catch (err) {
        showToast(err.message, "error");
      } finally {
        setIsDeletingId(null);
      }
    }
  };

  const handleInputChange = (fieldKey, value) => {
    setFormData(prev => {
      const updated = { ...prev, [fieldKey]: value };
      
      if (fieldKey === "RENT_AMOUNT") {
        updated["RENT_AMOUNT_WORDS"] = numberToWords(value);
      } else if (fieldKey === "DEPOSIT_AMOUNT") {
        updated["DEPOSIT_AMOUNT_WORDS"] = numberToWords(value);
      } else if (fieldKey === "LEASE_PERIOD_NUM" && value === "11") {
        updated["LEASE_PERIOD"] = "eleven months";
      }
      
      return updated;
    });

    setChangedField(fieldKey);
    setTimeout(() => setChangedField(null), 600);
  };

  const handleSaveAndGenerate = (e) => {
    if (e) e.preventDefault();
    if (isGenerating) return;

    if (!fieldsConfig) {
      showToast("Template configuration is not loaded. Please wait.", "error");
      return;
    }

    // Collect all expected keys from metadata config
    const requiredKeys = [];
    Object.values(fieldsConfig).forEach(category => {
      Object.keys(category.fields).forEach(key => {
        requiredKeys.push(key);
      });
    });

    // Verify all keys are present and non-empty
    const missingOrEmpty = [];
    requiredKeys.forEach(key => {
      const val = formData[key];
      if (val === undefined || val === null || val.toString().trim() === "") {
        missingOrEmpty.push(key);
      }
    });

    if (missingOrEmpty.length > 0) {
      showToast("Please fill in all fields before generating.", "error");
      return;
    }

    setFilenameInput(editorTitle);
    setFeeInput(formData.SERVICE_FEE || "");
    setShowFilenameModal(true);
  };

  const handleConfirmGeneration = async () => {
    if (!filenameInput.trim()) {
      showToast("Please enter a valid filename.", "error");
      return;
    }
    
    setShowFilenameModal(false);
    const finalTitle = filenameInput.trim();
    setEditorTitle(finalTitle);

    const finalFee = isAdmin ? feeInput.trim() : (formData.SERVICE_FEE || "");
    setFormData(prev => ({ ...prev, SERVICE_FEE: finalFee }));

    await executeSaveAndGenerate(finalTitle, finalFee);
  };

  const executeSaveAndGenerate = async (titleToSave, feeToSave = "") => {
    setIsGenerating(true);
    setActivePreviewTab("pdf");

    try {
      const payload = {
        id: editorId,
        title: titleToSave,
        data: {
          ...formData,
          SERVICE_FEE: feeToSave,
          AGREEMENT_CONDITIONS: agreementConditions
            .filter(c => c.checked)
            .map(c => c.text)
        }
      };

      const res = await fetch("/api/agreements", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${authToken}`
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Failed to generate document.");
      }

      const data = await res.json();
      
      const timestamp = new Date().getTime();
      if (iframeRef.current) {
        iframeRef.current.src = `${data.pdfUrl}?token=${authToken}&t=${timestamp}`;
      }
      
      setDownloadUrls({ 
        docx: `${data.docxUrl}?token=${authToken}`, 
        pdf: `${data.pdfUrl}?token=${authToken}` 
      });
      setEditorId(data.id);
      setPdfGenerated(true);
      fetchAgreements(); 
      showToast("Rental Agreement generated and saved successfully!", "success");
    } catch (err) {
      showToast(`Error: ${err.message}`, "error");
      setActivePreviewTab("draft");
    } finally {
      setIsGenerating(false);
    }
  };

  const handlePrint = () => {
    try {
      if (iframeRef.current && iframeRef.current.contentWindow) {
        iframeRef.current.contentWindow.focus();
        iframeRef.current.contentWindow.print();
      } else {
        throw new Error("Iframe window not accessible");
      }
    } catch {
      const printWindow = window.open(`${downloadUrls.pdf}`, "_blank");
      if (printWindow) {
        printWindow.onload = () => printWindow.print();
      } else {
        showToast("Pop-up blocked. Please enable popups or download PDF to print.", "error");
      }
    }
  };

  const renderHighlight = (fieldKey) => {
    const value = formData[fieldKey];
    const displayVal = value !== undefined && value !== null && value.trim() !== "" ? value : `[${fieldKey}]`;
    const isChanged = changedField === fieldKey;
    
    return (
      <span className={`bg-indigo-50 border-b-2 border-dashed border-indigo-400/80 px-1 rounded text-indigo-700 font-semibold transition-all duration-350 dark:bg-indigo-950/40 dark:border-indigo-500/50 dark:text-indigo-300 ${isChanged ? 'animate-pulse bg-amber-200/40 dark:bg-amber-500/30' : ''}`}>
        {displayVal}
      </span>
    );
  };

  // Calculations for dashboard indicators
  const totalAgreementsCount = agreements.length;
  
  const activeTenantsCount = agreements.filter(ag => {
    const endDate = parseLeaseEndDate(ag.data?.LEASE_END_DATE);
    if (!endDate) return true;
    return endDate >= new Date();
  }).length;

  const expiringCount = agreements.filter(ag => {
    const endDate = parseLeaseEndDate(ag.data?.LEASE_END_DATE);
    if (!endDate) return false;
    const diff = endDate.getTime() - new Date().getTime();
    const diffDays = Math.ceil(diff / (1000 * 60 * 60 * 24));
    return diffDays >= 0 && diffDays <= 30;
  }).length;

  // Only the admin can record/earn document creation charges
  const isAdmin = userProfile?.email === "admin@rentalpro.com";

  // Revenue = total earnings from preparing documents (admin service charges), NOT tenant rent
  const monthlyRevenueSum = agreements
    .reduce((sum, ag) => sum + parseCurrency(ag.data?.SERVICE_FEE), 0);

  // Dynamic Rent Inflow In 2026 (Jan-Jun)
  const monthsList = [
    { name: "Jan", index: 0 },
    { name: "Feb", index: 1 },
    { name: "Mar", index: 2 },
    { name: "Apr", index: 3 },
    { name: "May", index: 4 },
    { name: "Jun", index: 5 }
  ];

  const chartData = monthsList.map(m => {
    let sum = 0;
    agreements.forEach(ag => {
      const startDate = parseLeaseStartDate(ag.data?.AGREEMENT_DATE);
      const endDate = parseLeaseEndDate(ag.data?.LEASE_END_DATE);
      const rentVal = parseCurrency(ag.data?.RENT_AMOUNT);
      
      const monthStart = new Date(2026, m.index, 1);
      const monthEnd = new Date(2026, m.index + 1, 0); // Last day of month
      
      let isActiveInMonth = true;
      if (startDate) {
        if (startDate > monthEnd) {
          isActiveInMonth = false;
        }
      }
      if (endDate) {
        if (endDate < monthStart) {
          isActiveInMonth = false;
        }
      }
      
      if (isActiveInMonth) {
        sum += rentVal;
      }
    });
    return { name: m.name, value: sum };
  });

  const maxChartValue = Math.max(...chartData.map(d => d.value), 1000);

  // Dynamic {t("operationsJournal")}
  const journalLogs = [];
  const sortedAgs = [...agreements].sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
  
  sortedAgs.slice(0, 3).forEach(ag => {
    journalLogs.push({
      type: "draft",
      title: "New Agreement Drafted",
      desc: `${ag.data.OWNER_NAME || 'Owner'} drafted commercial shop lease for ${ag.data.TENANT_NAME || 'Tenant'}.`,
      color: "bg-emerald-500",
      textColor: "text-emerald-800 dark:text-emerald-400"
    });
  });

  // Expiry warnings
  agreements.forEach(ag => {
    if (isLeaseExpiring30D(ag)) {
      journalLogs.push({
        type: "expiry",
        title: "Expiry Alert Triggered",
        desc: `Agreement ${ag.title} expires in under 30 days (on ${ag.data.LEASE_END_DATE}).`,
        color: "bg-amber-500",
        textColor: "text-amber-800 dark:text-amber-400"
      });
    }
  });

  if (journalLogs.length === 0) {
    journalLogs.push({
      type: "draft",
      title: "No Activity Yet",
      desc: "Create your first rental agreement to see operational logs.",
      color: "bg-slate-400",
      textColor: "text-slate-600"
    });
  }

  // Filtered portfolio lists
  const getFilteredPortfolio = () => {
    return filteredAgreements.filter(ag => {
      if (portfolioFilter === "active") {
        return isLeaseActive(ag);
      }
      if (portfolioFilter === "expiring") {
        return isLeaseExpiring30D(ag);
      }
      if (portfolioFilter === "draft") {
        return !ag.data.TENANT_NAME || ag.title.toLowerCase().includes("draft");
      }
      return true; // "all"
    });
  };

  const filteredAgreements = agreements.filter(ag => 
    ag.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="relative min-h-screen bg-slate-50 text-slate-850 dark:bg-slate-950 dark:text-slate-100 transition-colors duration-250">
      
      {/* Background Gradient Blurs (Light/Dark tailored, vibrant & cool) */}
      <div className="absolute top-[10%] left-[20%] w-[500px] h-[500px] rounded-full bg-indigo-200/40 dark:bg-indigo-900/15 blur-[120px] pointer-events-none z-0" />
      <div className="absolute bottom-[10%] right-[10%] w-[400px] h-[400px] rounded-full bg-emerald-200/30 dark:bg-emerald-900/10 blur-[100px] pointer-events-none z-0" />

      {/* Toast System */}
      <div className={`fixed bottom-8 right-8 z-50 flex items-center gap-3 px-5 py-3.5 rounded-2xl border shadow-2xl backdrop-blur-xl transition-all duration-300 transform ${
        toast.show ? "opacity-100 translate-y-0 scale-100" : "opacity-0 translate-y-4 scale-95 pointer-events-none"
      } ${
        toast.type === "error" 
          ? "bg-rose-50 border-rose-200 text-rose-800 dark:bg-rose-950/90 dark:border-rose-500/40 dark:text-rose-200" 
          : toast.type === "success"
            ? "bg-emerald-50 border-emerald-200 text-emerald-800 dark:bg-emerald-950/90 dark:border-emerald-500/40 dark:text-emerald-200"
            : "bg-white border-slate-200 text-slate-800 dark:bg-slate-900/90 dark:border-slate-800 dark:text-slate-200"
      }`}>
        {toast.type === "error" && <AlertCircle className="w-5 h-5 text-rose-500 dark:text-rose-400" />}
        {toast.type === "success" && <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />}
        <span className="text-sm font-semibold">{toast.message}</span>
      </div>

      {/* View router: Login */}
      {currentView === "login" && (
        <div className="min-h-screen flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200/80 dark:bg-slate-900/60 dark:border-slate-800/80 backdrop-blur-xl p-8 rounded-3xl w-full max-w-md shadow-xl dark:shadow-2xl space-y-6 relative z-10 transition-all">
            <div className="flex flex-col items-center gap-3 text-center">
              <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 dark:bg-emerald-500/15 dark:border-emerald-500/30 rounded-2xl">
                <FileSignature className="w-8 h-8 text-emerald-650 dark:text-emerald-450" />
              </div>
              <h1 className="text-2xl font-extrabold text-slate-800 dark:text-slate-100">{t("welcomeBack")}</h1>
              <p className="text-sm text-slate-500 dark:text-slate-400">{t("welcomeSub")}</p>
            </div>

            <form onSubmit={handleLogin} className="space-y-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-500 dark:text-slate-400 flex items-center gap-1.5 uppercase tracking-wider">
                  <Mail className="w-3.5 h-3.5 text-slate-400" /> {t("emailAddress")}
                </label>
                <input
                  type="email"
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  className="bg-slate-50 border border-slate-200 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950/60 dark:text-slate-200 text-sm"
                  placeholder="e.g. admin@rentalpro.com"
                  required
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-500 dark:text-slate-400 flex items-center gap-1.5 uppercase tracking-wider">
                  <Lock className="w-3.5 h-3.5 text-slate-400" /> {t("password")}
                </label>
                <input
                  type="password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  className="bg-slate-50 border border-slate-200 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950/60 dark:text-slate-200 text-sm"
                  placeholder="••••••••"
                  required
                />
              </div>

              <button
                type="submit"
                className="w-full bg-emerald-600 hover:bg-emerald-700 text-white dark:bg-emerald-500 dark:hover:bg-emerald-650 dark:text-slate-950 font-bold py-3 rounded-xl shadow-lg shadow-emerald-500/10 hover:shadow-emerald-500/20 active:scale-[0.98] transition-all cursor-pointer text-center text-sm"
              >
                Log In
              </button>
            </form>

            <div className="border-t border-slate-100 dark:border-slate-800 pt-4 text-center">
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {t("dontHaveAccount")}{" "}
                <button 
                  onClick={() => setCurrentView("register")}
                  className="text-emerald-600 dark:text-emerald-400 hover:underline font-bold"
                >
                  {t("signUp")}
                </button>
              </p>
              
              <div className="mt-4 text-[11px] text-slate-500 bg-slate-50 dark:bg-slate-950/40 border border-slate-200 dark:border-slate-800/60 p-3 rounded-xl leading-relaxed text-left">
                🔑 Demo credentials:
                <div className="mt-1"><span className="font-semibold text-emerald-700 dark:text-emerald-400">admin@rentalpro.com</span> (pw: <span className="font-medium text-slate-700 dark:text-slate-300">admin123</span>)</div>
                <div><span className="font-semibold text-emerald-700 dark:text-emerald-400">tenant@rentalpro.com</span> (pw: <span className="font-medium text-slate-700 dark:text-slate-300">tenant123</span>)</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* View router: Register */}
      {currentView === "register" && (
        <div className="min-h-screen flex items-center justify-center p-4">
          <div className="bg-white border border-slate-200 dark:bg-slate-900/60 dark:border-slate-800/80 backdrop-blur-xl p-8 rounded-3xl w-full max-w-md shadow-xl dark:shadow-2xl space-y-6 relative z-10 transition-all">
            <div className="flex flex-col items-center gap-3 text-center">
              <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 dark:bg-emerald-500/15 dark:border-emerald-500/30 rounded-2xl">
                <UserPlus className="w-8 h-8 text-emerald-600 dark:text-emerald-500" />
              </div>
              <h1 className="text-2xl font-extrabold text-slate-800 dark:text-slate-100">{t("createAccount")}</h1>
              <p className="text-sm text-slate-500 dark:text-slate-400">Sign up to manage and store custom templates.</p>
            </div>

            <form onSubmit={handleRegister} className="space-y-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-500 dark:text-slate-400 flex items-center gap-1.5 uppercase tracking-wider">
                  <UserIcon className="w-3.5 h-3.5 text-slate-400" /> {t("fullName")}
                </label>
                <input
                  type="text"
                  value={regName}
                  onChange={(e) => setRegName(e.target.value)}
                  className="bg-slate-50 border border-slate-200 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950/60 dark:text-slate-200 text-sm"
                  placeholder="e.g. John Doe"
                  required
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-500 dark:text-slate-400 flex items-center gap-1.5 uppercase tracking-wider">
                  <Mail className="w-3.5 h-3.5 text-slate-400" /> {t("emailAddress")}
                </label>
                <input
                  type="email"
                  value={regEmail}
                  onChange={(e) => setRegEmail(e.target.value)}
                  className="bg-slate-50 border border-slate-200 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950/60 dark:text-slate-200 text-sm"
                  placeholder="e.g. john@example.com"
                  required
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-500 dark:text-slate-400 flex items-center gap-1.5 uppercase tracking-wider">
                  <Lock className="w-3.5 h-3.5 text-slate-400" /> {t("password")}
                </label>
                <input
                  type="password"
                  value={regPassword}
                  onChange={(e) => setRegPassword(e.target.value)}
                  className="bg-slate-50 border border-slate-200 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950/60 dark:text-slate-200 text-sm"
                  placeholder="••••••••"
                  required
                />
              </div>

              <button
                type="submit"
                className="w-full bg-emerald-600 hover:bg-emerald-700 text-white dark:bg-emerald-500 dark:hover:bg-emerald-650 dark:text-slate-950 font-bold py-3 rounded-xl shadow-lg shadow-emerald-500/10 hover:shadow-emerald-500/20 active:scale-[0.98] transition-all cursor-pointer text-center text-sm"
              >
                {t("signUp")}
              </button>
            </form>

            <div className="border-t border-slate-100 dark:border-slate-800 pt-4 text-center">
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {t("alreadyHaveAccount")}{" "}
                <button 
                  onClick={() => setCurrentView("login")}
                  className="text-emerald-600 dark:text-emerald-400 hover:underline font-bold"
                >
                  Log In
                </button>
              </p>
            </div>
          </div>
        </div>
      )}
      {/* View router: Dashboard */}
      {currentView === "dashboard" && (
        <div className="flex min-h-screen bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-100 transition-colors duration-250">
          
          {/* Left Sidebar */}
          <aside className="w-[280px] bg-slate-950 text-slate-400 flex flex-col justify-between border-r border-slate-900 z-10 flex-shrink-0 py-6 px-4">
            <div className="space-y-8">
              {/* Sidebar Header / Brand */}
              <div className="flex items-center justify-between px-2">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-emerald-500/10 border border-emerald-500/25 rounded-xl">
                    <FileSignature className="w-5 h-5 text-emerald-500" />
                  </div>
                  <span className="text-base font-extrabold text-white tracking-tight">
                    {t("brandName")}
                  </span>
                </div>
                <button className="text-slate-500 hover:text-slate-300">
                  <Plus className="w-4 h-4 rotate-45" />
                </button>
              </div>

              {/* Navigation Menu */}
              <nav className="space-y-1">
                {[
                  { id: "dashboard", label: t("dashboard"), icon: () => <SlidersHorizontal className="w-4 h-4" /> },
                  { id: "templates", label: t("templates"), icon: () => <Folder className="w-4 h-4" /> },
                  { id: "conditions", label: t("conditions"), icon: () => <CheckCircle2 className="w-4 h-4" /> },
                  { id: "tenants", label: t("tenants"), icon: () => <Users className="w-4 h-4" /> },
                  { id: "owners", label: t("owners"), icon: () => <UserIcon className="w-4 h-4" /> },
                  { id: "assets", label: t("assets"), icon: () => <Building className="w-4 h-4" /> },
                  { id: "analytics", label: t("analytics"), icon: () => <TrendingUp className="w-4 h-4" /> },
                  { id: "settings", label: t("settings"), icon: () => <Settings className="w-4 h-4" /> },
                  { id: "print", label: t("print"), icon: () => <Layers className="w-4 h-4" /> }
                ].map((item) => {
                  const isActive = activeSidebarTab === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => setActiveSidebarTab(item.id)}
                      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                        isActive 
                          ? "bg-[#0f9770] text-white shadow-lg shadow-emerald-950/20" 
                          : "hover:bg-slate-900/60 hover:text-slate-200"
                      }`}
                    >
                      {item.icon()}
                      {t(item.id)}
                    </button>
                  );
                })}
              </nav>
            </div>

            {/* Sidebar Footer */}
            <div className="px-2">
              <button 
                onClick={handleLogout}
                className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold text-rose-500 hover:bg-rose-500/5 hover:text-rose-400 transition-all"
              >
                <LogOut className="w-4 h-4" />
                {t("signOut")}
              </button>
            </div>
          </aside>

          {/* Right Content Pane */}
          <div className="flex-grow bg-[#f8fafc] text-slate-850 dark:bg-slate-950 dark:text-slate-100 flex flex-col min-h-screen relative overflow-x-hidden">
            
            {/* Background Blur Overlays for premium look */}
            <div className="absolute top-[5%] left-[10%] w-[350px] h-[350px] rounded-full bg-indigo-500/5 dark:bg-indigo-500/10 blur-[80px] pointer-events-none z-0" />
            <div className="absolute bottom-[20%] right-[5%] w-[300px] h-[300px] rounded-full bg-emerald-500/5 dark:bg-emerald-500/5 blur-[70px] pointer-events-none z-0" />

            {/* Topbar Console Navigation */}
            <header className="flex justify-between items-center py-4 px-8 border-b border-slate-200/80 bg-white/70 dark:bg-slate-950/70 dark:border-slate-800 backdrop-blur-md sticky top-0 z-20 flex-shrink-0">
              {/* Search Console */}
              <div className="relative w-80">
                <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder={t("searchAgreements")}
                  className="bg-slate-50 border border-slate-200/60 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 focus:bg-white text-slate-800 text-sm rounded-xl pl-10 pr-4 py-2 w-full outline-none transition-all dark:bg-slate-900/60 dark:border-slate-800 dark:focus:bg-slate-900/60 dark:text-slate-200"
                />
              </div>

              {/* User and Controls Area */}
              <div className="flex items-center gap-4">
                {/* Language Pill */}
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
                </button>

                {/* Notifications Bell */}
                <div className="relative">
                  <button 
                    onClick={() => {
                      setShowNotifications(!showNotifications);
                      setHasNewNotifications(false);
                    }}
                    className="p-2 rounded-xl bg-white border border-slate-200/60 shadow-sm hover:border-slate-300 dark:bg-slate-900/40 dark:border-slate-800 text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-white relative active:scale-95 transition-all cursor-pointer"
                  >
                    <Bell className="w-4 h-4" />
                    {hasNewNotifications && (
                      <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-rose-500 ring-2 ring-white dark:ring-slate-900" />
                    )}
                  </button>

                  {/* Dropdown Panel */}
                  {showNotifications && (
                    <div className="absolute right-0 mt-2 w-80 bg-white border border-slate-200/85 rounded-2xl shadow-xl dark:bg-slate-900 dark:border-slate-800 py-3.5 px-4 text-left z-30 space-y-3">
                      <div className="flex justify-between items-center border-b pb-2 border-slate-100 dark:border-slate-800">
                        <span className="text-xs font-extrabold text-slate-800 dark:text-white uppercase tracking-wider">Notifications</span>
                        <button 
                          onClick={() => setShowNotifications(false)}
                          className="text-[10px] font-bold text-slate-400 hover:text-slate-600 dark:text-slate-500 dark:hover:text-slate-300"
                        >
                          Close
                        </button>
                      </div>
                      <div className="space-y-2.5 max-h-48 overflow-y-auto">
                        <div className="text-[11px] leading-relaxed border-b pb-2 border-slate-50 dark:border-slate-800/40 last:border-b-0">
                          <span className="font-bold text-slate-700 dark:text-slate-200">Verification Approved</span>
                          <p className="text-slate-400 mt-0.5">Aadhar credentials for tenant verified successfully.</p>
                        </div>
                        <div className="text-[11px] leading-relaxed border-b pb-2 border-slate-50 dark:border-slate-800/40 last:border-b-0">
                          <span className="font-bold text-slate-700 dark:text-slate-200">System Ready</span>
                          <p className="text-slate-400 mt-0.5">{t("welcomeBack")} Builder active console.</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Theme Toggle */}
                <button 
                  onClick={toggleTheme}
                  className="p-2 rounded-xl bg-white border border-slate-200/60 shadow-sm dark:bg-slate-900/40 dark:border-slate-800 text-slate-500 hover:text-slate-700 dark:hover:text-white active:scale-95 transition-all"
                  title="Toggle Theme"
                >
                  {theme === "light" ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4 text-amber-400" />}
                </button>

                {/* Vertical Divider */}
                <div className="h-6 w-[1px] bg-slate-200 dark:bg-slate-800" />

                {/* User Card */}
                <div className="flex items-center gap-2.5">
                  <div className="w-9 h-9 rounded-xl bg-[#0f9770] text-white flex items-center justify-center font-bold text-sm shadow-sm shadow-emerald-500/10">
                    {userProfile?.full_name?.charAt(0).toUpperCase() || "A"}
                  </div>
                  <div className="hidden sm:flex flex-col text-left leading-none">
                    <span className="text-xs font-bold text-slate-800 dark:text-slate-100">{userProfile?.full_name || "Admin Console"}</span>
                    <span className="text-[10px] text-slate-400 dark:text-slate-500 font-semibold mt-0.5">{userProfile?.email || "admin@rentalpro.com"}</span>
                  </div>
                </div>
              </div>
            </header>

            {/* Main Content Area */}
            <main className="p-8 flex-grow space-y-8 z-10">
              
              {activeSidebarTab === "dashboard" && (
                <>
                  {/* Dashboard Content Header */}
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <div className="text-left">
                      <h1 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight flex items-center gap-2">
                        {t("dashboardHeader")}
                        <Sparkles className="w-5 h-5 text-emerald-500 animate-pulse" />
                      </h1>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                        {t("dashboardSub")}
                      </p>
                    </div>

                    <button
                      onClick={startNewAgreement}
                      className="bg-[#0f9770] hover:bg-[#0d8563] text-white font-bold px-5 py-2.5 rounded-xl shadow-md shadow-emerald-500/10 hover:shadow-emerald-500/20 transition-all active:scale-[0.98] flex items-center justify-center gap-2 cursor-pointer text-sm"
                    >
                      <Plus className="w-4.5 h-4.5" />
                      {t("newRentalAgreement")}
                    </button>
                  </div>

                  {/* Indicators Row */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    
                    {/* Metric 1: Agreements */}
                    <div className="bg-white border border-slate-200/80 p-5 rounded-2xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800/80 flex items-center justify-between">
                      <div className="text-left space-y-1.5">
                        <span className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">
                          {t("agreements")}
                        </span>
                        <h3 className="text-3xl font-extrabold text-slate-800 dark:text-white">
                          {totalAgreementsCount}
                        </h3>
                        <div className="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1">
                          <span>{t("cloudSecured")}</span>
                        </div>
                      </div>
                      <div className="p-3 bg-emerald-500/10 rounded-xl text-emerald-600 dark:bg-emerald-500/15 dark:text-emerald-400">
                        <FileText className="w-5 h-5" />
                      </div>
                    </div>

                    {/* Metric 2: {t("activeTenants")} */}
                    <div className="bg-white border border-slate-200/80 p-5 rounded-2xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800/80 flex items-center justify-between">
                      <div className="text-left space-y-1.5">
                        <span className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">
                          {t("activeTenants")}
                        </span>
                        <h3 className="text-3xl font-extrabold text-slate-800 dark:text-white">
                          {activeTenantsCount}
                        </h3>
                        <div className="text-[10px] text-indigo-600 dark:text-indigo-400 font-bold">
                          <span>{t("liveRelationships")}</span>
                        </div>
                      </div>
                      <div className="p-3 bg-indigo-500/10 rounded-xl text-indigo-600 dark:bg-indigo-500/15 dark:text-indigo-400">
                        <Users className="w-5 h-5" />
                      </div>
                    </div>

                    {/* Metric 3: Expiring */}
                    <div className="bg-white border border-slate-200/80 p-5 rounded-2xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800/80 flex items-center justify-between">
                      <div className="text-left space-y-1.5">
                        <span className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">
                          {t("expiring30d")}
                        </span>
                        <h3 className="text-3xl font-extrabold text-slate-800 dark:text-white">
                          {expiringCount}
                        </h3>
                        <div className="text-[10px] text-amber-600 dark:text-amber-400 font-bold">
                          <span>{t("requiresRenewal")}</span>
                        </div>
                      </div>
                      <div className="p-3 bg-amber-500/10 rounded-xl text-amber-600 dark:bg-amber-500/15 dark:text-amber-400">
                        <AlertTriangle className="w-5 h-5" />
                      </div>
                    </div>

                    {/* Metric 4: {t("monthlyRevenue")} */}
                    <div className="bg-white border border-slate-200/80 p-5 rounded-2xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800/80 flex items-center justify-between">
                      <div className="text-left space-y-1.5">
                        <span className="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">
                          Document Earnings
                        </span>
                        <h3 className="text-3xl font-extrabold text-slate-800 dark:text-white">
                          ₹{monthlyRevenueSum.toLocaleString("en-IN")}
                        </h3>
                        <div className="text-[10px] text-purple-600 dark:text-purple-400 font-bold">
                          <span>Earned from preparing documents</span>
                        </div>
                      </div>
                      <div className="p-3 bg-purple-500/10 rounded-xl text-purple-600 dark:bg-purple-500/15 dark:text-purple-400">
                        <IndianRupee className="w-5 h-5" />
                      </div>
                    </div>

                  </div>

                  {/* Workspace Middle Panel (Chart & Journal logs) */}
                  <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6">
                    
                    {/* 1. Monthly Rent Inflow Chart Card */}
                    <div className="bg-white border border-slate-200/80 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800/80 flex flex-col justify-between h-[360px]">
                      <div className="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-4">
                        <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider text-left">
                          {t("monthlyRentInflow")}
                        </h3>
                        <span className="text-[10px] font-bold text-slate-500 bg-slate-50 border border-slate-200/60 px-2.5 py-0.5 rounded-lg dark:bg-slate-950 dark:border-slate-800">
                          {t("year2026")}
                        </span>
                      </div>

                      {/* Chart Visualizer */}
                      <div className="flex-grow flex items-end justify-between px-4 py-6 h-48 relative z-10">
                        {chartData.map((d, i) => {
                          const barPercent = maxChartValue > 0 ? (d.value / maxChartValue) * 100 : 0;
                          return (
                            <div key={i} className="flex flex-col items-center gap-2 flex-grow group max-w-[64px]">
                              {/* Tooltip on hover */}
                              <div className="opacity-0 group-hover:opacity-100 transition-opacity bg-slate-900 text-white text-[10px] font-extrabold px-2 py-1 rounded absolute -top-1 shadow dark:bg-slate-800 z-30 pointer-events-none transform -translate-y-2">
                                ₹{d.value.toLocaleString("en-IN")}
                              </div>
                              
                              {/* Bar Graphic */}
                              <div className="w-full bg-slate-100 rounded-xl h-40 dark:bg-slate-950 flex items-end overflow-hidden border border-slate-200/10">
                                <div 
                                  className="w-full bg-[#0f9770] rounded-t-xl hover:bg-[#0d8563] transition-all duration-500 cursor-pointer"
                                  style={{ height: `${Math.max(barPercent, 4)}%` }}
                                />
                              </div>
                              <span className="text-xs font-semibold text-slate-400 dark:text-slate-500">{d.name}</span>
                            </div>
                          );
                        })}
                      </div>
                    </div>

                    {/* 2. {t("operationsJournal")} Card */}
                    <div className="bg-white border border-slate-200/80 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800/80 flex flex-col justify-between h-[360px]">
                      <div className="border-b border-slate-100 dark:border-slate-800 pb-4">
                        <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider text-left">
                          {t("operationsJournal")}
                        </h3>
                      </div>

                      {/* Journal Feed */}
                      <div className="flex-grow overflow-y-auto py-4 space-y-4 pr-1 text-left">
                        {journalLogs.slice(0, 3).map((log, index) => (
                          <div key={index} className="flex gap-3 items-start text-xs border-b border-slate-50 dark:border-slate-850/20 pb-3 last:border-b-0">
                            <span className={`w-2.5 h-2.5 rounded-full ${log.color} mt-1 flex-shrink-0`} />
                            <div className="space-y-0.5 leading-snug">
                              <h4 className="font-bold text-slate-750 dark:text-slate-200">{log.title}</h4>
                              <p className="text-[11px] text-slate-450 dark:text-slate-400 font-medium">{log.desc}</p>
                            </div>
                          </div>
                        ))}
                      </div>

                      <button className="w-full py-2.5 border border-slate-200/80 rounded-xl text-xs font-bold text-slate-700 hover:bg-slate-50 dark:border-slate-850 dark:text-slate-300 dark:hover:bg-slate-900/50 transition-all">
                        {t("manageVerifications")}
                      </button>
                    </div>

                  </div>

                  {/* Portfolio Workspace List */}
                  <div className="bg-white border border-slate-200/80 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800/80 space-y-6">
                    
                    {/* Portfolio header & filters */}
                    <div className="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-4 border-b border-slate-100 dark:border-slate-800 pb-5">
                      <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider text-left">
                        {t("portfolio")}
                      </h3>
                      
                      {/* Portfolio Filters */}
                      <div className="flex bg-slate-100 border border-slate-200/80 p-1 rounded-xl dark:bg-slate-950 dark:border-slate-800 self-end">
                        {[
                          { id: "all", label: t("all") },
                          { id: "active", label: t("active") },
                          { id: "expiring", label: t("expiring") },
                          { id: "draft", label: t("draft") }
                        ].map((tab) => {
                          const isTabActive = portfolioFilter === tab.id;
                          return (
                            <button
                              key={tab.id}
                              onClick={() => setPortfolioFilter(tab.id)}
                              className={`text-xs font-bold px-4 py-1.5 rounded-lg transition-all ${
                                isTabActive 
                                  ? "bg-white text-slate-850 shadow dark:bg-slate-900 dark:text-white" 
                                  : "text-slate-400 hover:text-slate-600 dark:text-slate-500 dark:hover:text-slate-350"
                              }`}
                            >
                              {t(tab.id)}
                            </button>
                          );
                        })}
                      </div>
                    </div>

                    {/* Portfolio list Grid */}
                    {isDataLoading ? (
                      <div className="flex flex-col items-center justify-center py-12 gap-3 text-slate-400">
                        <Loader2 className="w-8 h-8 animate-spin text-emerald-500" />
                        <span className="text-sm">Refreshing Portfolio...</span>
                      </div>
                    ) : getFilteredPortfolio().length === 0 ? (
                      <div className="flex flex-col items-center justify-center py-16 gap-3 text-center">
                        <div className="w-12 h-12 rounded-full bg-slate-50 border border-slate-200/60 flex items-center justify-center text-slate-400 dark:bg-slate-900 dark:border-slate-800 dark:text-slate-600">
                          <FileText className="w-6 h-6" />
                        </div>
                        <div>
                          <h4 className="text-sm font-bold text-slate-700 dark:text-slate-350">No agreements found</h4>
                          <p className="text-[11px] text-slate-400 dark:text-slate-500 mt-0.5">
                            There are no customized documents in this category.
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                        {getFilteredPortfolio().map(agreement => (
                          <div 
                            key={agreement.id}
                            className="bg-white border border-slate-200/80 hover:border-slate-300 p-5 rounded-2xl transition-all duration-200 shadow-sm hover:shadow-md dark:bg-slate-900/40 dark:border-slate-800 dark:hover:border-slate-750 dark:shadow-none flex flex-col justify-between gap-4"
                          >
                            <div>
                              <div className="flex justify-between items-start gap-4">
                                <h3 className="font-bold text-slate-800 dark:text-slate-200 line-clamp-1 text-left">
                                  {agreement.title}
                                </h3>
                                <span className="text-[10px] font-bold text-slate-500 bg-slate-50 border border-slate-200 dark:bg-slate-950 dark:border-slate-800 px-2.5 py-0.5 rounded-full whitespace-nowrap">
                                  ID: {agreement.id}
                                </span>
                              </div>
                              
                              <p className="text-[11px] text-slate-400 dark:text-slate-500 mt-1 text-left">
                                Updated {new Date(agreement.updated_at).toLocaleDateString()} at {new Date(agreement.updated_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                              </p>

                              <div className="mt-4 flex flex-wrap gap-x-4 gap-y-2 text-[11px] text-slate-600 bg-slate-50 border border-slate-100 p-2.5 rounded-xl dark:text-slate-400 dark:bg-slate-950/30 dark:border-slate-800/50 text-left">
                                <div><span className="text-slate-400 dark:text-slate-500">Tenant:</span> <span className="font-bold text-slate-700 dark:text-slate-300">{agreement.data.TENANT_NAME || "Not set"}</span></div>
                                <div><span className="text-slate-400 dark:text-slate-500">Rent:</span> <span className="font-bold text-slate-700 dark:text-slate-300">Rs {agreement.data.RENT_AMOUNT || "0"}</span></div>
                              </div>
                            </div>

                            <div className="flex justify-between items-center border-t border-slate-100 dark:border-slate-800 pt-3 flex-wrap gap-2">
                              <div className="flex gap-2">
                                <button
                                  onClick={() => editAgreement(agreement)}
                                  className="flex items-center gap-1.5 text-xs text-slate-600 hover:text-emerald-700 px-3 py-1.5 rounded-lg border border-slate-200 hover:border-emerald-355 hover:bg-emerald-50 bg-white transition-all cursor-pointer dark:text-slate-400 dark:hover:text-emerald-400 dark:border-slate-800 dark:hover:border-emerald-500/20 dark:bg-slate-950 dark:hover:bg-emerald-50/5"
                                >
                                  <Edit2 className="w-3.5 h-3.5" />
                                  Edit
                                </button>
                                <button
                                  onClick={() => deleteAgreement(agreement.id)}
                                  disabled={isDeletingId === agreement.id}
                                  className="flex items-center gap-1.5 text-xs text-slate-600 hover:text-rose-600 px-3 py-1.5 rounded-lg border border-slate-200 hover:border-rose-300 hover:bg-rose-50 bg-white disabled:opacity-50 transition-all cursor-pointer dark:text-slate-400 dark:hover:text-rose-400 dark:border-slate-800 dark:hover:border-rose-500/20 dark:bg-slate-950 dark:hover:bg-rose-50/5 disabled:cursor-not-allowed"
                                >
                                  {isDeletingId === agreement.id ? (
                                    <Loader2 className="w-3.5 h-3.5 animate-spin text-rose-500" />
                                  ) : (
                                    <Trash2 className="w-3.5 h-3.5" />
                                  )}
                                  Delete
                                </button>
                              </div>

                              <div className="flex gap-3">
                                <a
                                  href={`${agreement.docx_url}&token=${authToken}`}
                                  download={`${agreement.title}.docx`}
                                  className="flex items-center gap-1 text-[11px] font-bold text-slate-500 hover:text-slate-850 dark:text-slate-400 dark:hover:text-slate-200"
                                >
                                  <FileDown className="w-3.5 h-3.5" />
                                  DOCX
                                </a>
                                <a
                                  href={`${agreement.pdf_url}&token=${authToken}`}
                                  download={`${agreement.title}.pdf`}
                                  className="flex items-center gap-1 text-[11px] font-bold text-slate-500 hover:text-slate-850 dark:text-slate-400 dark:hover:text-slate-200"
                                >
                                  <FileDown className="w-3.5 h-3.5" />
                                  PDF
                                </a>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </>
              )}

              {activeSidebarTab === "conditions" && (
                <div className="space-y-6 text-left animate-fade-in">
                  <div>
                    <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">{t("masterClauseHeader")}</h2>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">{t("masterClauseSub")}</p>
                  </div>

                  <div className="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-805 space-y-6">
                    <div className="space-y-4">
                      {masterConditions.map((condition, index) => (
                        <div key={index} className="flex items-start gap-4 p-4 bg-slate-50 dark:bg-slate-950/40 border border-slate-200/60 dark:border-slate-800 rounded-2xl group transition-all">
                          <span className="w-6 h-6 rounded-full bg-emerald-500/10 text-emerald-600 dark:bg-emerald-500/15 dark:text-emerald-400 flex items-center justify-center font-bold text-xs flex-shrink-0 mt-0.5">
                            {index + 1}
                          </span>
                          
                          <div className="flex-grow">
                            <textarea
                              value={condition}
                              onChange={(e) => {
                                const updated = [...masterConditions];
                                updated[index] = e.target.value;
                                updateMasterConditionsState(updated);
                              }}
                              className="w-full bg-transparent text-sm font-semibold text-slate-700 dark:text-slate-300 outline-none resize-none border-b border-transparent focus:border-slate-200 dark:focus:border-slate-800 focus:bg-white dark:focus:bg-slate-950/40 p-1 rounded transition-all min-h-[60px]"
                            />
                            <div className="flex gap-2 mt-1.5 text-[10px] text-slate-400 font-medium">
                              <span>Placeholders detected:</span>
                              <span className="text-indigo-650 dark:text-indigo-400 font-semibold">
                                {(condition.match(/\{\{([A-Z0-9_]+)\}\}/g) || []).join(", ") || "None"}
                              </span>
                            </div>
                          </div>

                          <button
                            type="button"
                            onClick={() => {
                              if (window.confirm("Are you sure you want to delete this global clause?")) {
                                const updated = masterConditions.filter((_, idx) => idx !== index);
                                updateMasterConditionsState(updated);
                                showToast("Global clause removed.", "success");
                              }
                            }}
                            className="p-2 text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-all opacity-0 group-hover:opacity-100"
                            title="Delete Global Clause"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      ))}
                    </div>

                    <div className="border-t border-slate-100 dark:border-slate-800 pt-5 space-y-4">
                      <h3 className="text-sm font-bold text-slate-800 dark:text-white">{t("createNewMaster")}</h3>
                      <div className="flex gap-3">
                        <textarea
                          id="newMasterClauseText"
                          placeholder={t("masterClausePlaceholder")}
                          className="flex-grow bg-slate-50 border border-slate-205 focus:border-[#0f9770] focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all resize-none h-20 dark:bg-slate-950/60 dark:border-slate-800 dark:focus:border-emerald-500 dark:text-slate-200"
                        />
                        <button
                          type="button"
                          onClick={() => {
                            const textarea = document.getElementById("newMasterClauseText");
                            const text = textarea ? textarea.value.trim() : "";
                            if (!text) {
                              showToast("Please type a clause to add.", "error");
                              return;
                            }
                            const updated = [...masterConditions, text];
                            updateMasterConditionsState(updated);
                            if (textarea) textarea.value = "";
                            showToast("New global clause added successfully!", "success");
                          }}
                          className="bg-[#0f9770] hover:bg-[#0d8563] text-white font-bold px-5 py-2.5 rounded-xl shadow-md transition-all active:scale-[0.98] flex items-center justify-center gap-2 text-xs self-end h-fit cursor-pointer"
                        >
                          <Plus className="w-4 h-4" />
                          {t("addGlobalClause")}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeSidebarTab === "templates" && (
                <div className="space-y-6 text-left">
                  <div>
                    <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">{t("legalTemplates")}</h2>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">{t("templatesSub")}</p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div className="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800 flex flex-col justify-between h-[280px]">
                      <div className="space-y-3">
                        <div className="p-3 bg-emerald-500/10 rounded-2xl w-fit text-emerald-600 dark:bg-emerald-500/15 dark:text-emerald-400">
                          <Building className="w-6 h-6" />
                        </div>
                        <h3 className="font-extrabold text-slate-800 dark:text-white text-base">{t("commercialRentalAgreement")}</h3>
                        <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                          {t("commercialRentalSub")}
                        </p>
                      </div>
                      <button
                        onClick={startNewAgreement}
                        className="w-full mt-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2.5 rounded-xl shadow-md transition-all active:scale-[0.98] text-xs cursor-pointer"
                      >
                        {t("customizeGenerate")}
                      </button>
                    </div>

                    <div className="bg-white border border-slate-200/50 p-6 rounded-3xl shadow-sm dark:bg-slate-900/10 dark:border-slate-800/50 flex flex-col justify-between h-[280px] opacity-75">
                      <div className="space-y-3">
                        <div className="p-3 bg-slate-500/10 rounded-2xl w-fit text-slate-500 dark:bg-slate-800 dark:text-slate-400">
                          <Users className="w-6 h-6" />
                        </div>
                        <div className="flex items-center justify-between">
                          <h3 className="font-extrabold text-slate-800 dark:text-white text-base">Residential Rent Agreement</h3>
                          <span className="text-[9px] font-extrabold text-indigo-600 bg-indigo-50 dark:text-indigo-400 dark:bg-indigo-950 px-2 py-0.5 rounded-full uppercase">Coming Soon</span>
                        </div>
                        <p className="text-xs text-slate-400 dark:text-slate-500 leading-relaxed">
                          Legal format for residential apartments and houses with terms customized for tenants and flat owners.
                        </p>
                      </div>
                      <button disabled className="w-full mt-4 bg-slate-200 text-slate-450 dark:bg-slate-800 dark:text-slate-600 font-bold py-2.5 rounded-xl text-xs cursor-not-allowed">
                        Coming Soon
                      </button>
                    </div>

                    <div className="bg-white border border-slate-200/50 p-6 rounded-3xl shadow-sm dark:bg-slate-900/10 dark:border-slate-800/50 flex flex-col justify-between h-[280px] opacity-75">
                      <div className="space-y-3">
                        <div className="p-3 bg-slate-500/10 rounded-2xl w-fit text-slate-500 dark:bg-slate-800 dark:text-slate-400">
                          <FileText className="w-6 h-6" />
                        </div>
                        <div className="flex items-center justify-between">
                          <h3 className="font-extrabold text-slate-800 dark:text-white text-base">Mutual NDA</h3>
                          <span className="text-[9px] font-extrabold text-indigo-600 bg-indigo-50 dark:text-indigo-400 dark:bg-indigo-950 px-2 py-0.5 rounded-full uppercase">Coming Soon</span>
                        </div>
                        <p className="text-xs text-slate-400 dark:text-slate-500 leading-relaxed">
                          Confidentiality contract designed to safeguard sensitive IP, trade secrets, and operational data.
                        </p>
                      </div>
                      <button disabled className="w-full mt-4 bg-slate-200 text-slate-450 dark:bg-slate-800 dark:text-slate-600 font-bold py-2.5 rounded-xl text-xs cursor-not-allowed">
                        Coming Soon
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {activeSidebarTab === "tenants" && (
                <div className="space-y-6 text-left">
                  <div className="flex justify-between items-center">
                    <div>
                      <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">Tenant Management & Verification</h2>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Track current tenants, verify credentials, and run background checks.</p>
                    </div>
                    <button 
                      onClick={() => showToast("Launching background verification portal...", "info")}
                      className="bg-[#0f9770] hover:bg-[#0d8563] text-white text-xs font-bold px-4 py-2.5 rounded-xl transition-all shadow-md active:scale-95 cursor-pointer"
                    >
                      Run New Verification
                    </button>
                  </div>

                  <div className="bg-white border border-slate-200 rounded-3xl dark:bg-slate-900/40 dark:border-slate-800 overflow-hidden shadow-sm">
                    <div className="overflow-x-auto">
                      <table className="w-full border-collapse">
                        <thead>
                          <tr className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/20 text-slate-400 text-[10px] font-extrabold uppercase tracking-wider">
                            <th className="px-6 py-4 text-left">Tenant Name</th>
                            <th className="px-6 py-4 text-left">Parent/Guardian</th>
                            <th className="px-6 py-4 text-left">Age</th>
                            <th className="px-6 py-4 text-left">Address</th>
                            <th className="px-6 py-4 text-left">Verification Status</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-350">
                          {agreements.map((ag, index) => (
                            <tr key={index} className="hover:bg-slate-50/50 dark:hover:bg-slate-900/30">
                              <td className="px-6 py-4 font-bold text-slate-800 dark:text-white">{ag.data.TENANT_NAME || "Not Set"}</td>
                              <td className="px-6 py-4">{ag.data.TENANT_PARENT || "Not Set"}</td>
                              <td className="px-6 py-4">{ag.data.TENANT_AGE || "N/A"}</td>
                              <td className="px-6 py-4 max-w-xs truncate">{ag.data.TENANT_ADDRESS || "Not Set"}</td>
                              <td className="px-6 py-4">
                                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-400 border border-emerald-200/40">
                                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                                  Aadhar Verified
                                </span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}

              {activeSidebarTab === "owners" && (
                <div className="space-y-6 text-left">
                  <div>
                    <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">Owners Registry</h2>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Management index for property owners and landlords.</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {agreements.map((ag, index) => (
                      <div key={index} className="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800 flex flex-col gap-4">
                        <div className="flex justify-between items-start">
                          <div className="space-y-1">
                            <h3 className="font-extrabold text-slate-800 dark:text-white text-base">{ag.data.OWNER_NAME || "Not Set"}</h3>
                            <p className="text-[11px] text-slate-400">{ag.data.OWNER_PARENT || "Not Set"}</p>
                          </div>
                          <span className="text-[10px] font-bold text-slate-500 bg-slate-50 border border-slate-200 dark:bg-slate-950 dark:border-slate-800 px-2.5 py-0.5 rounded-full">Owner</span>
                        </div>
                        
                        <div className="text-xs space-y-2 border-t border-slate-100 dark:border-slate-800 pt-3">
                          <div><span className="text-slate-400 font-bold">Age:</span> <span className="font-bold text-slate-700 dark:text-slate-300">{ag.data.OWNER_AGE || "N/A"}</span></div>
                          <div>
                            <span className="text-slate-400 font-bold">Registered Address:</span> 
                            <p className="font-medium text-slate-600 dark:text-slate-350 mt-0.5 leading-relaxed">{ag.data.OWNER_ADDRESS || "Not Set"}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeSidebarTab === "assets" && (
                <div className="space-y-6 text-left">
                  <div>
                    <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">Property Assets Directory</h2>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Track rental premises, retail spaces, and commercial amenities.</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {agreements.map((ag, index) => (
                      <div key={index} className="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800 flex flex-col gap-3">
                        <div className="flex justify-between items-center">
                          <h3 className="font-extrabold text-slate-800 dark:text-white text-base">{ag.data.BUSINESS_NAME || "Commercial Outlet"}</h3>
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-700 dark:bg-indigo-950/50 dark:text-indigo-400 border border-indigo-200/40">Active Premises</span>
                        </div>

                        <div className="text-xs space-y-2 pt-2 border-t border-slate-100 dark:border-slate-800">
                          <div>
                            <span className="text-slate-400 font-bold">Premises Address:</span> 
                            <p className="font-semibold text-slate-700 dark:text-slate-300 mt-0.5 leading-relaxed">{ag.data.PREMISES_ADDRESS || "Not Set"}</p>
                          </div>
                          <div>
                            <span className="text-slate-400 font-bold">Amenities & Details:</span> 
                            <p className="font-medium text-slate-500 dark:text-slate-400 mt-0.5 leading-relaxed">{ag.data.PREMISES_DESCRIPTION || "Not Set"}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeSidebarTab === "analytics" && (
                <div className="space-y-6 text-left">
                  <div>
                    <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">Analytics & Revenue Console</h2>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Detailed rent inflow aggregations and performance metrics.</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800 space-y-4">
                      <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider border-b pb-3 border-slate-100 dark:border-slate-800">Revenue Stream (Jan-Jun 2026)</h3>
                      <div className="space-y-3">
                        {chartData.map((d, index) => (
                          <div key={index} className="flex justify-between items-center text-xs font-semibold">
                            <span className="text-slate-400">{d.name} 2026</span>
                            <span className="text-slate-800 dark:text-white font-bold">₹{d.value.toLocaleString("en-IN")}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800 space-y-4">
                      <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider border-b pb-3 border-slate-100 dark:border-slate-800">Performance Ratios</h3>
                      <div className="space-y-4 pt-2">
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-slate-450 font-semibold">Total Document Earnings</span>
                          <span className="text-lg font-extrabold text-[#0f9770]">₹{monthlyRevenueSum.toLocaleString("en-IN")}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-slate-450 font-semibold">Security Deposits Managed</span>
                          <span className="text-base font-bold text-indigo-600 dark:text-indigo-400">
                            ₹{agreements.reduce((sum, ag) => sum + parseCurrency(ag.data?.DEPOSIT_AMOUNT), 0).toLocaleString("en-IN")}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-slate-450 font-semibold">{t("activeTenants")} Ratio</span>
                          <span className="text-xs font-extrabold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-100 dark:border-emerald-900/45">100% Active</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeSidebarTab === "settings" && (
                <div className="space-y-6 text-left">
                  <div>
                    <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">App Settings</h2>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Configure parameters, brand details, and print outputs.</p>
                  </div>

                  <div className="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800 space-y-6 max-w-2xl">
                    <div className="space-y-4">
                      <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider">Custom Layout Preferences</h3>
                      
                      <div className="flex items-center justify-between border-b pb-3 border-slate-100 dark:border-slate-800">
                        <div className="space-y-0.5">
                          <span className="text-xs font-bold text-slate-700 dark:text-slate-200">Default Stamp Duty Sheet</span>
                          <p className="text-[11px] text-slate-400">Set standard layout margins for printable pages</p>
                        </div>
                        <select className="bg-slate-50 border border-slate-200 dark:bg-slate-950 dark:border-slate-800 text-xs font-bold rounded-lg px-2.5 py-1.5 outline-none text-slate-700 dark:text-slate-300">
                          <option>Karnataka (Rs. 200 Stamp)</option>
                          <option>Delhi (Rs. 100 Stamp)</option>
                          <option>Maharashtra (Rs. 500 Stamp)</option>
                        </select>
                      </div>

                      <div className="flex items-center justify-between border-b pb-3 border-slate-100 dark:border-slate-800">
                        <div className="space-y-0.5">
                          <span className="text-xs font-bold text-slate-700 dark:text-slate-200">Export Word Formatting</span>
                          <p className="text-[11px] text-slate-400">Apply custom fonts (e.g. Times New Roman, Arial)</p>
                        </div>
                        <span className="text-xs font-bold text-slate-500 bg-slate-50 dark:bg-slate-950 px-2 py-1 rounded border dark:border-slate-800">Times New Roman (12pt)</span>
                      </div>
                    </div>
                    
                    <button 
                      onClick={() => showToast("Settings saved successfully.", "success")}
                      className="bg-[#0f9770] hover:bg-[#0d8563] text-white text-xs font-bold px-5 py-2.5 rounded-xl transition-all shadow-md active:scale-95 cursor-pointer"
                    >
                      Save Configuration
                    </button>
                  </div>

                  <div className="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800 space-y-4 max-w-2xl">
                    <div className="flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-[#0f9770]" />
                      <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider">Software Updates</h3>
                    </div>

                    <div className="flex items-center justify-between border-b pb-3 border-slate-100 dark:border-slate-800">
                      <div className="space-y-0.5">
                        <span className="text-xs font-bold text-slate-700 dark:text-slate-200">Current Version</span>
                        <p className="text-[11px] text-slate-400">Check online for the latest release</p>
                      </div>
                      <span className="text-xs font-bold text-slate-500 bg-slate-50 dark:bg-slate-950 px-2 py-1 rounded border dark:border-slate-800">
                        v{updateInfo?.current || "—"}
                      </span>
                    </div>

                    {updateInfo && updateInfo.enabled === false && (
                      <p className="text-[11px] text-slate-400 flex items-center gap-1.5">
                        <AlertCircle className="w-3.5 h-3.5" />
                        Automatic updates are available only in the installed desktop app.
                      </p>
                    )}

                    {updateInfo?.enabled && !updateInfo.available && (
                      <p className="text-[11px] text-emerald-600 dark:text-emerald-400 font-semibold flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        You're running the latest version.
                      </p>
                    )}

                    {updateInfo?.available && (
                      <div className="bg-emerald-50 border border-emerald-200 dark:bg-emerald-950/30 dark:border-emerald-800/50 rounded-xl p-3.5 space-y-2">
                        <p className="text-xs font-bold text-emerald-800 dark:text-emerald-300">
                          New version available: v{updateInfo.latest}
                        </p>
                        {updateInfo.notes && (
                          <p className="text-[11px] text-emerald-700/80 dark:text-emerald-400/80 whitespace-pre-line">
                            {updateInfo.notes}
                          </p>
                        )}
                      </div>
                    )}

                    <div className="flex items-center gap-3">
                      <button
                        onClick={checkForUpdates}
                        disabled={checkingUpdate || applyingUpdate}
                        className="bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-bold px-4 py-2.5 rounded-xl transition-all active:scale-95 cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2"
                      >
                        {checkingUpdate && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                        {checkingUpdate ? "Checking…" : "Check for Updates"}
                      </button>

                      {updateInfo?.available && (
                        <button
                          onClick={applyUpdate}
                          disabled={applyingUpdate}
                          className="bg-[#0f9770] hover:bg-[#0d8563] text-white text-xs font-bold px-5 py-2.5 rounded-xl transition-all shadow-md active:scale-95 cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2"
                        >
                          {applyingUpdate && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                          {applyingUpdate ? "Updating…" : "Update Now & Restart"}
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {activeSidebarTab === "print" && (
                <div className="space-y-6 text-left">
                  <div>
                    <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">Test Print Comparison Console</h2>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Validate PDF dimensions and compare layout margins side-by-side.</p>
                  </div>

                  <div className="bg-white border border-slate-200 p-6 rounded-3xl shadow-sm dark:bg-slate-900/40 dark:border-slate-800 max-w-2xl space-y-4">
                    <h3 className="text-sm font-extrabold text-slate-800 dark:text-white uppercase tracking-wider">Word-to-PDF Engine Quality Controls</h3>
                    <p className="text-xs text-slate-500 leading-relaxed dark:text-slate-400">
                      Our printing engine uses native Microsoft Word COM automation to convert draft XML contents directly to PDF, ensuring zero layout shift or character overlaps compared to raw HTML rendering systems.
                    </p>
                    
                    <div className="grid grid-cols-2 gap-4 text-xs font-bold pt-2">
                      <div className="p-4 bg-slate-50 dark:bg-slate-950/60 rounded-2xl border dark:border-slate-800">
                        <span className="text-slate-400">Print Margins</span>
                        <p className="text-slate-800 dark:text-white mt-1">1 inch (Standard Letter)</p>
                      </div>
                      <div className="p-4 bg-slate-50 dark:bg-slate-950/60 rounded-2xl border dark:border-slate-800">
                        <span className="text-slate-400">Font Optimization</span>
                        <p className="text-slate-800 dark:text-white mt-1">Subpixel antialiased TrueType</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </main>
          </div>
        </div>
      )}
      {/* View router: Customizer Editor */}
      {currentView === "editor" && (
        <div className={`mx-auto flex flex-col h-screen relative z-10 transition-all duration-300 ${
          fullscreenMode !== "none" ? "w-screen max-w-none p-0 bg-slate-50 dark:bg-slate-950" : "max-w-[1600px] p-6"
        }`}>
          
          {/* Floating Control Bar in Fullscreen Mode */}
          {fullscreenMode !== "none" && (
            <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 px-4 py-2 rounded-2xl bg-white/80 border border-slate-200/80 shadow-2xl backdrop-blur-xl dark:bg-slate-900/80 dark:border-slate-800 transition-all hover:scale-[1.02] duration-200">
              <span className="text-[10px] font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-widest mr-2 border-r pr-3 border-slate-200 dark:border-slate-800">
                Fullscreen Mode
              </span>
              
              <button
                type="button"
                onClick={() => setFullscreenMode("split")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  fullscreenMode === "split"
                    ? "bg-[#0f9770] text-white shadow-md shadow-emerald-500/10"
                    : "text-slate-500 hover:bg-slate-100 hover:text-slate-800 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white"
                }`}
                title="Split View (Form + Document)"
              >
                <SlidersHorizontal className="w-3.5 h-3.5" />
                <span>Split View</span>
              </button>

              <button
                type="button"
                onClick={() => setFullscreenMode("document")}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  fullscreenMode === "document"
                    ? "bg-[#0f9770] text-white shadow-md shadow-emerald-500/10"
                    : "text-slate-500 hover:bg-slate-100 hover:text-slate-800 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white"
                }`}
                title="Document Only View"
              >
                <Eye className="w-3.5 h-3.5" />
                <span>Document View</span>
              </button>

              <div className="h-4 w-[1px] bg-slate-200 dark:bg-slate-805 mx-1" />

              <button
                type="button"
                onClick={() => setFullscreenMode("none")}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-rose-600 hover:bg-rose-50 dark:text-rose-400 dark:hover:bg-rose-950/30 transition-all"
                title="Exit Fullscreen"
              >
                <LogOut className="w-3.5 h-3.5 rotate-180" />
                <span>Exit</span>
              </button>
            </div>
          )}

          {/* Editor Header */}
          {fullscreenMode === "none" && (
            <header className="flex justify-between items-center py-4 border-b border-slate-200 dark:border-slate-800 flex-shrink-0">
              <div className="flex items-center gap-3">
                <button
                  onClick={() => {
                    setFullscreenMode("none");
                    setCurrentView("dashboard");
                  }}
                  className="p-2.5 rounded-xl border border-slate-200 hover:border-slate-300 bg-white text-slate-500 hover:text-slate-800 active:scale-95 transition-all shadow-sm dark:border-slate-800 dark:hover:border-slate-700 dark:bg-slate-900/60 dark:text-slate-400 dark:hover:text-slate-200 dark:shadow-none"
                  title="Back to Dashboard"
                >
                  <ArrowLeft className="w-4 h-4" />
                </button>
                
                <div className="flex flex-col gap-0.5">
                  <input
                    type="text"
                    value={editorTitle}
                    onChange={(e) => setEditorTitle(e.target.value)}
                    className="bg-transparent text-lg font-extrabold text-slate-850 border-b border-transparent focus:border-slate-300 outline-none max-w-sm px-1 dark:text-slate-100 dark:focus:border-slate-800"
                    placeholder="Enter agreement title..."
                    required
                  />
                  <span className="text-[10px] text-slate-405 font-bold px-1 dark:text-slate-500 uppercase tracking-wider">
                    {editorId ? `Editing Agreement ID: ${editorId}` : "Drafting New Document"}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <button
                  onClick={() => setFullscreenMode("split")}
                  className="p-2.5 rounded-xl border border-slate-200 hover:border-slate-300 bg-white text-slate-500 hover:text-slate-800 dark:border-slate-800 dark:hover:border-slate-700 dark:bg-slate-900/60 dark:text-slate-400 dark:hover:text-slate-200 active:scale-95 transition-all shadow-sm dark:shadow-none"
                  title="Enter Fullscreen Mode"
                >
                  <Maximize2 className="w-4 h-4" />
                </button>

                <button 
                  onClick={toggleTheme}
                  className="p-2.5 rounded-xl border border-slate-200 hover:border-slate-300 bg-white text-slate-500 hover:text-slate-700 dark:border-slate-800 dark:hover:border-slate-700 dark:bg-slate-900/60 dark:text-slate-400 dark:hover:text-slate-200 active:scale-95 transition-all shadow-sm dark:shadow-none"
                  title="Toggle Theme"
                >
                  {theme === "light" ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4 text-amber-400" />}
                </button>
              </div>
            </header>
          )}

          {/* Editor Workspace */}
          <main className={`grid gap-6 flex-grow min-h-0 transition-all duration-300 ${
            fullscreenMode !== "none" ? "p-4 py-4" : "py-6"
          } ${
            fullscreenMode === "document" 
              ? "grid-cols-1" 
              : showConditionsSidebar 
                ? "grid-cols-1 lg:grid-cols-[400px_360px_1fr]" 
                : "grid-cols-1 lg:grid-cols-[450px_1fr]"
          }`}>
            
            {/* Left panel: Inputs */}
            {fullscreenMode !== "document" && (<>
              <section className="bg-white border border-slate-200 rounded-3xl flex flex-col min-h-0 shadow-sm dark:bg-slate-900/40 dark:border-slate-800 dark:shadow-none overflow-hidden">
                <div className="p-5 border-b border-slate-100 dark:border-slate-800 flex-shrink-0">
                <h2 className="text-base font-bold flex items-center gap-2 text-slate-800 dark:text-slate-200">
                  <SlidersHorizontal className="w-4.5 h-4.5 text-emerald-655 dark:text-emerald-500" />
                  {t("customizeDetails")}
                </h2>
                <p className="text-[11px] text-slate-500 mt-1 dark:text-slate-400">
                  {t("customizeSub")}
                </p>
              </div>
              
              <form onSubmit={handleSaveAndGenerate} className="flex-grow overflow-y-auto p-5 space-y-5">
                {!fieldsConfig ? (
                  <div className="flex flex-col items-center justify-center py-12 gap-3 text-slate-400">
                    <Loader2 className="w-8 h-8 animate-spin text-emerald-500" />
                    <span>Loading fields configuration...</span>
                  </div>
                ) : (
                  Object.entries(fieldsConfig).map(([catKey, category]) => (
                    <div key={catKey} className="bg-slate-50 border border-slate-200 hover:border-slate-305 rounded-2xl p-4 transition-colors dark:bg-slate-900/60 dark:border-slate-800/60 dark:hover:border-slate-800">
                      <h3 className="text-[11px] font-extrabold text-emerald-700 uppercase tracking-widest border-b border-slate-200 pb-2 mb-3 dark:text-emerald-500 dark:border-slate-800">
                        {category.title}
                      </h3>
                      
                      <div className="space-y-4">
                        {Object.entries(category.fields).map(([fieldKey, field]) => (
                          <div key={fieldKey} className="flex flex-col gap-1.5">
                            <label htmlFor={fieldKey} className="text-xs font-bold text-slate-600 dark:text-slate-400">
                              {field.label}
                            </label>
                            {field.type === "textarea" ? (
                              <textarea
                                id={fieldKey}
                                value={formData[fieldKey] || ""}
                                onChange={(e) => handleInputChange(fieldKey, e.target.value)}
                                className="bg-white border border-slate-200 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 text-slate-850 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all resize-none h-20 dark:bg-slate-950/60 dark:border-slate-800 dark:focus:border-emerald-500 dark:text-slate-200"
                                placeholder={field.placeholder}
                                required
                              />
                            ) : (
                              <input
                                type={field.type}
                                id={fieldKey}
                                value={formData[fieldKey] || ""}
                                onChange={(e) => handleInputChange(fieldKey, e.target.value)}
                                className="bg-white border border-slate-200 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 text-slate-850 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:border-emerald-500 dark:text-slate-200"
                                placeholder={field.placeholder}
                                required
                              />
                            )}
                          </div>
                        ))}
                      </div>

                      {/* Terms & Conditions Checklist Summary Card under Financials */}
                      {catKey === "FINANCIALS" && (
                        <div className="mt-6 border-t border-slate-200 dark:border-slate-800 pt-5 space-y-4 text-left">
                          <div className="flex justify-between items-center">
                            <h4 className="text-xs font-extrabold text-slate-800 dark:text-white uppercase tracking-wider flex items-center gap-1.5">
                              <CheckCircle2 className="w-4 h-4 text-[#0f9770]" />
                              {t("leaseConditions")}
                            </h4>
                            <span className="text-[10px] font-bold bg-emerald-500/10 text-emerald-700 dark:text-emerald-450 px-2 py-0.5 rounded-full">
                              {agreementConditions.filter(c => c.checked).length} of {agreementConditions.length} Active
                            </span>
                          </div>

                          <div className="bg-white border border-slate-200/80 rounded-2xl p-4 dark:bg-slate-950/20 dark:border-slate-800 space-y-4">
                            <div className="space-y-2.5 max-h-[160px] overflow-y-auto pr-1">
                              {agreementConditions.filter(c => c.checked).map((cond, idx) => (
                                <div key={cond.id || idx} className="flex gap-2 items-start text-[11px] text-slate-650 dark:text-slate-400 font-semibold leading-relaxed">
                                  <span className="text-emerald-505 text-xs flex-shrink-0 mt-0.5">✓</span>
                                  <span className="line-clamp-2">{cond.text}</span>
                                </div>
                              ))}
                              {agreementConditions.filter(c => c.checked).length === 0 && (
                                <span className="text-slate-400 text-xs block py-2 text-center">No active conditions for this agreement.</span>
                              )}
                            </div>

                            <button
                              type="button"
                              onClick={() => setShowConditionsSidebar(prev => !prev)}
                              className={`w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl text-xs font-bold transition-all shadow-md active:scale-[0.98] cursor-pointer ${
                                showConditionsSidebar
                                  ? "bg-slate-800 text-white hover:bg-slate-850 shadow-slate-900/10 dark:bg-slate-700 dark:hover:bg-slate-650"
                                  : "bg-[#0f9770] text-white hover:bg-[#0d8563] shadow-emerald-500/10"
                              }`}
                            >
                              <SlidersHorizontal className="w-3.5 h-3.5" />
                              <span>{showConditionsSidebar ? t("hidePanel") : t("manageLeaseConditions")}</span>
                            </button>
                          </div>

                          {/* Quick add custom condition field */}
                          <div className="bg-slate-50 border border-slate-200/60 rounded-2xl p-3.5 dark:bg-slate-950/10 dark:border-slate-805 space-y-3">
                            <span className="text-[10px] font-extrabold text-slate-405 uppercase tracking-wider block">{t("quickAddClause")}</span>
                            <div className="flex gap-2">
                              <textarea
                                id="quickClauseText"
                                placeholder="E.g., The TENANT should pay the rent without delays..."
                                className="flex-grow bg-white border border-slate-200 focus:border-[#0f9770] text-xs rounded-xl px-2.5 py-1.5 outline-none transition-all resize-none h-11 dark:bg-slate-950/60 dark:border-slate-800 dark:text-slate-200"
                              />
                              <button
                                type="button"
                                onClick={() => {
                                  const textarea = document.getElementById("quickClauseText");
                                  const text = textarea ? textarea.value.trim() : "";
                                  if (!text) {
                                    showToast("Please enter clause text.", "error");
                                    return;
                                  }
                                  const newClause = {
                                    id: `custom-${Date.now()}`,
                                    text: text,
                                    checked: true
                                  };
                                  setAgreementConditions(prev => [...prev, newClause]);
                                  showToast("Clause added to this agreement.", "success");
                                  if (textarea) textarea.value = "";
                                }}
                                className="bg-[#0f9770] hover:bg-[#0d8563] text-white font-bold px-3 py-2 rounded-xl text-xs flex items-center justify-center shadow-md shadow-emerald-500/10 transition-all active:scale-[0.98] self-end cursor-pointer h-fit"
                              >
                                Add
                              </button>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))
                )}
              </form>
            </section>
            
            {/* Middle panel: {t("leaseConditions")} Sidebar */}
            {showConditionsSidebar && (
              <section className="bg-white border border-slate-200 rounded-3xl flex flex-col min-h-0 shadow-sm dark:bg-slate-900/40 dark:border-slate-800 dark:shadow-none overflow-hidden text-left animate-fade-in">
                {/* Header */}
                <div className="p-5 border-b border-slate-105 dark:border-slate-800 flex justify-between items-center flex-shrink-0">
                  <div>
                    <h3 className="text-sm font-extrabold text-slate-800 dark:text-slate-200 flex items-center gap-1.5 uppercase tracking-wider">
                      <CheckCircle2 className="w-4 h-4 text-[#0f9770]" />
                      {t("leaseConditions")}
                    </h3>
                    <p className="text-[10px] text-slate-500 mt-0.5 dark:text-slate-400">{t("sidebarSub")}</p>
                  </div>
                  <button
                    type="button"
                    onClick={() => setShowConditionsSidebar(false)}
                    className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-205 p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                    title="Close Sidebar"
                  >
                    <Plus className="w-4 h-4 rotate-45" />
                  </button>
                </div>

                {/* Search Bar */}
                <div className="p-3 border-b border-slate-105 dark:border-slate-800 flex-shrink-0">
                  <div className="relative">
                    <Search className="absolute left-3 top-2.5 w-3.5 h-3.5 text-slate-400" />
                    <input
                      type="text"
                      placeholder={t("searchClauses")}
                      value={clauseSearchQuery}
                      onChange={(e) => setClauseSearchQuery(e.target.value)}
                      className="w-full bg-slate-50 border border-slate-200 text-xs rounded-xl pl-9 pr-3 py-2 outline-none focus:border-emerald-500 focus:bg-white transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:text-slate-200 dark:focus:border-emerald-500"
                    />
                  </div>
                </div>

                {/* Checklist Container */}
                <div className="flex-grow overflow-y-auto p-4 space-y-3">
                  {agreementConditions
                    .filter(c => !clauseSearchQuery || c.text.toLowerCase().includes(clauseSearchQuery.toLowerCase()))
                    .map((cond) => {
                      const placeholders = cond.text.match(/\{\{([A-Z0-9_]+)\}\}/g) || [];
                      const originalIdx = agreementConditions.findIndex(item => item.id === cond.id);
                      
                      return (
                        <div key={cond.id} className="flex gap-2.5 items-start p-3 bg-slate-50 border border-slate-200/60 rounded-2xl dark:bg-slate-950/20 dark:border-slate-800 group hover:border-slate-300 dark:hover:border-slate-700 transition-all">
                          <input
                            type="checkbox"
                            checked={cond.checked}
                            onChange={(e) => {
                              const updated = [...agreementConditions];
                              updated[originalIdx].checked = e.target.checked;
                              setAgreementConditions(updated);
                            }}
                            className="mt-1 accent-emerald-600 rounded cursor-pointer flex-shrink-0"
                          />
                          
                          <div className="flex-grow min-w-0">
                            <textarea
                              value={cond.text}
                              onChange={(e) => {
                                const updated = [...agreementConditions];
                                updated[originalIdx].text = e.target.value;
                                setAgreementConditions(updated);
                              }}
                              className="w-full bg-transparent text-xs text-slate-700 dark:text-slate-305 outline-none resize-none border-b border-transparent focus:border-slate-200 dark:focus:border-slate-805 focus:bg-white dark:focus:bg-slate-900/60 p-1 rounded min-h-[50px] leading-relaxed"
                            />
                            
                            {placeholders.length > 0 && (
                              <div className="flex flex-wrap gap-1 mt-1 text-[8px] font-semibold text-slate-400">
                                <span className="text-slate-500 uppercase">Tags:</span>
                                {placeholders.map((ph, pi) => (
                                  <span key={pi} className="text-emerald-700 dark:text-emerald-400 bg-emerald-500/10 px-1 py-0.5 rounded">
                                    {ph.replace(/[{}]/g, "")}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>

                          <button
                            type="button"
                            onClick={() => {
                              const updated = agreementConditions.filter((_, idx) => idx !== originalIdx);
                              setAgreementConditions(updated);
                            }}
                            className="text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 p-1 rounded transition-colors flex-shrink-0 opacity-0 group-hover:opacity-100"
                            title="Remove Clause"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      );
                    })}
                  
                  {agreementConditions.filter(c => !clauseSearchQuery || c.text.toLowerCase().includes(clauseSearchQuery.toLowerCase())).length === 0 && (
                    <div className="text-center py-6 text-slate-405 text-xs dark:text-slate-500">
                      No conditions found.
                    </div>
                  )}
                </div>

                {/* Quick Add at bottom of sidebar */}
                <div className="p-4 border-t border-slate-100 bg-slate-50/50 dark:border-slate-800 dark:bg-slate-900/20 flex-shrink-0 space-y-3">
                  <span className="text-[9px] font-extrabold text-slate-500 uppercase tracking-wider">{t("createCustomClause")}</span>
                  <textarea
                    id="sidebarClauseText"
                    placeholder="E.g., The TENANT should maintain the premises clean..."
                    className="w-full bg-white border border-slate-200 focus:border-[#0f9770] text-xs rounded-xl px-3 py-2 outline-none transition-all resize-none h-14 dark:bg-slate-950/60 dark:border-slate-850 dark:text-slate-200"
                  />
                  <div className="flex justify-between items-center">
                    <label className="flex items-center gap-1.5 text-[9px] font-extrabold text-slate-500 cursor-pointer">
                      <input
                        id="sidebarSaveToMasterCheckbox"
                        type="checkbox"
                        defaultChecked={true}
                        className="accent-emerald-600 rounded"
                      />
                      {t("addGlobally")}
                    </label>
                    
                    <button
                      type="button"
                      onClick={() => {
                        const textarea = document.getElementById("sidebarClauseText");
                        const text = textarea ? textarea.value.trim() : "";
                        if (!text) {
                          showToast("Please enter clause text.", "error");
                          return;
                        }
                        
                        const newClause = {
                          id: `custom-${Date.now()}`,
                          text: text,
                          checked: true
                        };
                        const updatedAgreement = [...agreementConditions, newClause];
                        setAgreementConditions(updatedAgreement);
                        
                        const saveToMaster = document.getElementById("sidebarSaveToMasterCheckbox")?.checked;
                        if (saveToMaster) {
                          const updatedMaster = [...masterConditions, text];
                          updateMasterConditionsState(updatedMaster);
                          showToast("Clause added to agreement and global registry!", "success");
                        } else {
                          showToast("Clause added to this agreement.", "success");
                        }
                        
                        if (textarea) textarea.value = "";
                      }}
                      className="bg-[#0f9770] hover:bg-[#0d8563] text-white font-bold px-3 py-1.5 rounded-lg text-[10px] transition-all cursor-pointer shadow-md shadow-emerald-500/10 active:scale-95"
                    >
                      {t("addPoint")}
                    </button>
                  </div>
                  
                  <button
                    type="button"
                    onClick={() => {
                      if (window.confirm("Are you sure you want to reset all conditions for this agreement back to the global defaults?")) {
                        const resetConditions = masterConditions.map((masterText, idx) => ({
                          id: `master-${idx}-${Date.now()}`,
                          text: masterText,
                          checked: true
                        }));
                        setAgreementConditions(resetConditions);
                        showToast("Conditions reset to defaults.", "info");
                      }
                    }}
                    className="w-full text-center text-[9px] font-bold text-slate-405 hover:text-emerald-650 transition-colors uppercase pt-1"
                  >
                    {t("resetDefaults")}
                  </button>
                </div>
              </section>
            )}
            </>)}

            {/* Right panel: Preview */}
            <section className="bg-white border border-slate-200 rounded-3xl flex flex-col min-h-0 shadow-sm dark:bg-slate-900/40 dark:border-slate-800 dark:shadow-none overflow-hidden">
              <div className="p-5 border-b border-slate-100 dark:border-slate-800 flex-shrink-0 flex justify-between items-center flex-wrap gap-4">
                <div>
                  <h2 className="text-base font-bold flex items-center gap-2 text-slate-800 dark:text-slate-200">
                    <Eye className="w-4.5 h-4.5 text-emerald-600 dark:text-emerald-400" />
                    {t("docPreview")}
                  </h2>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
                    {t("previewSub")}
                  </p>
                </div>
                
                {/* View Toggler */}
                <div className="flex bg-slate-100 border border-slate-200 p-1 rounded-xl dark:bg-slate-950 dark:border-slate-800">
                  <button
                    type="button"
                    onClick={() => setActivePreviewTab("draft")}
                    className={`flex items-center gap-2 text-xs font-bold px-3.5 py-2 rounded-lg transition-all ${
                      activePreviewTab === "draft" 
                        ? "bg-emerald-600 text-white shadow dark:bg-emerald-500 dark:text-slate-950" 
                        : "text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
                    }`}
                  >
                    <FileText className="w-3.5 h-3.5" />
                    {t("draftText")}
                  </button>
                  <button
                    type="button"
                    onClick={() => pdfGenerated && setActivePreviewTab("pdf")}
                    disabled={!pdfGenerated}
                    className={`flex items-center gap-2 text-xs font-bold px-3.5 py-2 rounded-lg transition-all ${
                      activePreviewTab === "pdf" 
                        ? "bg-emerald-600 text-white shadow dark:bg-emerald-500 dark:text-slate-950" 
                        : "text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
                    } disabled:opacity-40 disabled:cursor-not-allowed`}
                  >
                    <FileSpreadsheet className="w-3.5 h-3.5" />
                    {t("pdfView")}
                  </button>
                </div>
              </div>

              {/* Viewport content */}
              <div className="flex-grow overflow-y-auto p-6 bg-slate-100/60 dark:bg-slate-950/40 flex justify-center items-start relative min-h-0 border-b border-slate-200 dark:border-slate-800">
                
                {/* HTML Draft View */}
                <div className={`w-full max-w-[800px] ${activePreviewTab === "draft" ? "block" : "hidden"}`}>
                  <div className="bg-white text-slate-900 px-12 py-14 shadow-xl border border-slate-200 rounded-xl rental-agreement-document text-justify text-[12pt] leading-[1.6]">
                    <h1 className="text-[18px] font-extrabold text-center underline mb-8 tracking-wider">
                      RENTAL AGREEMENT
                    </h1>
                    
                    <p className="mb-5 text-indent-0">
                      THIS RENTAL AGREEMENT is made and executed on this {renderHighlight("AGREEMENT_DATE")}, at {renderHighlight("AGREEMENT_PLACE")} by and between:
                    </p>
                    
                    <p className="mb-5">
                      <strong>{renderHighlight("OWNER_NAME")}</strong>, {renderHighlight("OWNER_PARENT")}, Aged {renderHighlight("OWNER_AGE")}, {renderHighlight("OWNER_ADDRESS")}, hereinafter called as the "OWNER", ONE PART,
                    </p>
                    
                    <p className="mb-5 font-bold text-center">AND</p>
                    
                    <p className="mb-5">
                      <strong>{renderHighlight("TENANT_NAME")}</strong> {renderHighlight("TENANT_PARENT")}, Aged {renderHighlight("TENANT_AGE")}, {renderHighlight("TENANT_ADDRESS")}, hereinafter called as the TENANT, SECOND PART.
                    </p>
                    
                    <p className="mb-5">
                      The TENANT has approached and requested the OWNER to rent out the building for Commercial Purpose {renderHighlight("PREMISES_ADDRESS")}, Consists {renderHighlight("PREMISES_DESCRIPTION")}, the Tenant has approached the owner let out the schedule shop premises for his {renderHighlight("BUSINESS_NAME")} for Commercial Purpose, The OWNER has agreed for the same.
                    </p>
                    
                    <p className="mb-5">
                      The OWNER and the TENANT are making this Rental Agreement on the following terms and conditions:
                    </p>
                    
                    <ol className="list-decimal pl-8 mb-5 space-y-3">
                      {agreementConditions
                        .filter(cond => cond.checked)
                        .map((cond, idx) => (
                          <li key={cond.id || idx} className="pl-2">
                            {renderClauseWithHighlights(cond.text)}
                          </li>
                        ))}
                    </ol>
                    
                    <p className="mb-5">
                      IN WITNESSES THEREOF THE OWNER and the TENANT have signed this rental agreement on the day, month and year mentioned above.
                    </p>
                    
                    <div className="mt-14 flex justify-between">
                      <div className="w-[45%] flex flex-col items-center">
                        <span className="border-b border-slate-900 w-full text-center pb-2 font-bold text-sm">
                          ({formData["OWNER_SIG_NAMES"] || "OWNER"})
                        </span>
                        <span className="mt-2 text-xs font-bold text-slate-800">OWNER</span>
                      </div>
                      <div className="w-[45%] flex flex-col items-center">
                        <span className="border-b border-slate-900 w-full text-center pb-2 font-bold text-sm">
                          ({formData["TENANT_SIG_NAMES"] || "TENANT"})
                        </span>
                        <span className="mt-2 text-xs font-bold text-slate-800">TENANT</span>
                      </div>
                    </div>
                    
                    <div className="mt-12 flex flex-col gap-2">
                      <h3 className="text-sm underline font-bold mb-1">Witnesses:</h3>
                      <p>1.</p>
                      <p>2.</p>
                    </div>
                  </div>
                </div>

                {/* PDF Frame */}
                <div className={`w-full h-full relative ${activePreviewTab === "pdf" && !showFilenameModal ? "flex flex-col" : "hidden"}`}>
                  {isGenerating && (
                    <div className="absolute inset-0 bg-white/90 backdrop-blur dark:bg-slate-950/85 flex flex-col justify-center items-center gap-3 z-20 rounded-2xl">
                      <Loader2 className="w-12 h-12 text-emerald-600 dark:text-emerald-400 animate-spin" />
                      <h3 className="font-bold text-lg text-emerald-800 dark:text-emerald-400">Saving & Generating PDF...</h3>
                      <p className="text-xs text-slate-500 max-w-[280px] text-center dark:text-slate-400">
                        Writing records to database and loading print layout...
                      </p>
                    </div>
                  )}
                  <iframe 
                    ref={iframeRef} 
                    src="" 
                    frameBorder="0" 
                    className="w-full h-full min-h-[600px] bg-slate-100 rounded-2xl border border-slate-200 dark:bg-slate-850 dark:border-slate-800 shadow-inner"
                  />
                </div>
              </div>

              {/* Action Bar */}
              <div className="p-5 bg-white dark:bg-slate-900/60 flex flex-wrap justify-between items-center gap-4 flex-shrink-0">
                <button 
                  type="submit" 
                  onClick={handleSaveAndGenerate}
                  disabled={isGenerating}
                  className="btn bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-600/50 text-white dark:bg-emerald-500 dark:hover:bg-emerald-600 dark:disabled:bg-emerald-500/50 dark:text-slate-950 text-sm font-bold px-6 py-3 rounded-xl shadow-md shadow-emerald-500/5 hover:shadow-emerald-500/15 active:scale-98 transition-all flex items-center gap-2 cursor-pointer disabled:cursor-not-allowed"
                >
                  {isGenerating ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileSignature className="w-4.5 h-4.5" />}
                  {t("saveGenerate")}
                </button>
                
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={handlePrint}
                    disabled={!pdfGenerated || isGenerating}
                    className="flex items-center gap-2 text-xs font-bold px-4 py-2.5 rounded-xl border border-slate-200 hover:border-slate-350 hover:bg-slate-55 bg-white text-slate-655 transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer dark:border-slate-800 dark:bg-slate-900 dark:hover:bg-slate-800 dark:text-slate-200"
                  >
                    <Printer className="w-3.5 h-3.5" />
                    Print
                  </button>
                  
                  <a
                    href={downloadUrls.docx}
                    download={`${editorTitle}.docx`}
                    className={`flex items-center gap-2 text-xs font-bold px-4 py-2.5 rounded-xl border border-slate-200 hover:border-slate-350 hover:bg-slate-55 bg-white text-slate-655 transition-colors ${
                      !pdfGenerated || isGenerating ? "opacity-50 cursor-not-allowed pointer-events-none" : ""
                    } dark:border-slate-800 dark:bg-slate-900 dark:hover:bg-slate-800 dark:text-slate-200`}
                  >
                    <FileDown className="w-3.5 h-3.5" />
                    {t("downloadDocx")}
                  </a>
                  
                  <a
                    href={downloadUrls.pdf}
                    download={`${editorTitle}.pdf`}
                    className={`flex items-center gap-2 text-xs font-bold px-4 py-2.5 rounded-xl border border-slate-200 hover:border-slate-350 hover:bg-slate-55 bg-white text-slate-655 transition-colors ${
                      !pdfGenerated || isGenerating ? "opacity-50 cursor-not-allowed pointer-events-none" : ""
                    } dark:border-slate-800 dark:bg-slate-900 dark:hover:bg-slate-800 dark:text-slate-200`}
                  >
                    <FileDown className="w-3.5 h-3.5" />
                    {t("downloadPdf")}
                  </a>
                </div>
              </div>
            </section>
          </main>
        </div>
      )}
      {/* Name Input Modal prior to PDF Generation */}
      {showFilenameModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm dark:bg-slate-950/80 transition-all duration-300">
          <div className="bg-white border border-slate-200/80 dark:bg-slate-900 dark:border-slate-800 rounded-3xl w-full max-w-md p-6 shadow-2xl space-y-5 transform transition-all scale-100 duration-200">
            <div className="space-y-2 text-left">
              <h3 className="text-base font-extrabold text-slate-800 dark:text-white flex items-center gap-2">
                <FileSignature className="w-5 h-5 text-[#0f9770]" />
                {t("nameYourDoc")}
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {t("nameDocSub")}
              </p>
            </div>

            <div className="flex flex-col gap-1.5 text-left">
              <label htmlFor="modalEditorTitle" className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                {t("docTitleLabel")}
              </label>
              <input
                id="modalEditorTitle"
                type="text"
                value={filenameInput}
                onChange={(e) => setFilenameInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    handleConfirmGeneration();
                  }
                }}
                className="bg-slate-55 border border-slate-200 focus:border-[#0f9770] focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                placeholder="e.g. Laggere Commercial Shop Lease"
                autoFocus
                required
              />
            </div>

            {isAdmin && (
              <div className="flex flex-col gap-1.5 text-left">
                <label htmlFor="modalServiceFee" className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                  <IndianRupee className="w-3.5 h-3.5 text-[#0f9770]" />
                  Document Charge
                  <span className="text-[9px] font-bold text-purple-600 bg-purple-500/10 px-1.5 py-0.5 rounded-md uppercase tracking-wide">Admin only</span>
                </label>
                <input
                  id="modalServiceFee"
                  type="text"
                  inputMode="numeric"
                  value={feeInput}
                  onChange={(e) => setFeeInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      handleConfirmGeneration();
                    }
                  }}
                  className="bg-slate-55 border border-slate-200 focus:border-[#0f9770] focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                  placeholder="e.g. 1500"
                />
                <p className="text-[10px] text-slate-400 dark:text-slate-500">
                  How much this document is created for (your earning). Counts toward revenue and is not printed in the document.
                </p>
              </div>
            )}

            <div className="flex justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setShowFilenameModal(false)}
                className="px-4 py-2 border border-slate-200 hover:border-slate-300 text-xs font-bold rounded-xl text-slate-500 hover:text-slate-800 bg-white transition-all dark:border-slate-800 dark:bg-slate-950 dark:text-slate-400 dark:hover:text-white cursor-pointer"
              >
                Cancel
              </button>
              
              <button
                type="button"
                onClick={handleConfirmGeneration}
                className="bg-[#0f9770] hover:bg-[#0d8563] text-white text-xs font-bold px-5 py-2.5 rounded-xl shadow-md transition-all active:scale-[0.97] cursor-pointer"
              >
                {t("generateSave")}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
