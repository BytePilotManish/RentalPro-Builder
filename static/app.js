document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const formCategories = document.getElementById("form-categories");
    const agreementForm = document.getElementById("agreement-form");
    const themeToggleBtn = document.getElementById("theme-toggle");
    const toggleDraftBtn = document.getElementById("toggle-draft");
    const togglePdfBtn = document.getElementById("toggle-pdf");
    const draftView = document.getElementById("draft-view");
    const pdfView = document.getElementById("pdf-view");
    const pdfIframe = document.getElementById("pdf-iframe");
    const pdfLoading = document.getElementById("pdf-loading");
    const generateBtn = document.getElementById("generate-btn");
    const printBtn = document.getElementById("print-btn");
    const downloadDocxBtn = document.getElementById("download-docx-btn");
    const downloadPdfBtn = document.getElementById("download-pdf-btn");
    const btnSpinner = document.getElementById("btn-spinner");
    const toast = document.getElementById("toast");
    const toastMessage = document.getElementById("toast-message");

    // State Variables
    let currentFields = {};
    let isGenerating = false;

    // Theme Management
    const initTheme = () => {
        const savedTheme = localStorage.getItem("theme") || "dark";
        document.documentElement.setAttribute("data-theme", savedTheme);
        updateThemeIcon(savedTheme);
    };

    const updateThemeIcon = (theme) => {
        const icon = themeToggleBtn.querySelector("i");
        if (theme === "light") {
            icon.className = "fa-solid fa-sun";
        } else {
            icon.className = "fa-solid fa-moon";
        }
    };

    themeToggleBtn.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "light" ? "dark" : "light";
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        updateThemeIcon(newTheme);
        showToast(`Switched to ${newTheme} mode`);
    });

    // Toast Notifications
    const showToast = (message, duration = 3000) => {
        toastMessage.textContent = message;
        toast.classList.remove("hide");
        setTimeout(() => {
            toast.classList.add("hide");
        }, duration);
    };

    // Live Preview Synchronization
    const updatePreviewHighlight = (fieldName, value) => {
        const highlights = document.querySelectorAll(`.highlight[data-field="${fieldName}"]`);
        
        // Handle special cases in preview formatting
        let formattedValue = value !== undefined && value !== null ? String(value) : "";
        if (formattedValue.trim() === "") {
            formattedValue = `[${fieldName}]`;
        }

        highlights.forEach(highlight => {
            // Only update text if it actually changed to prevent cursor flashing
            if (highlight.textContent !== formattedValue) {
                highlight.textContent = formattedValue;
                // Add minor flash animation class
                highlight.classList.add("changed");
                setTimeout(() => {
                    highlight.classList.remove("changed");
                }, 600);
            }
        });

        // Also check if signature blocks need updating (they are outside .highlight tags in some places)
        if (fieldName === "OWNER_SIG_NAMES") {
            const sigLine = document.querySelector(".sig-block:first-child .sig-line");
            if (sigLine) sigLine.textContent = `(${value || 'OWNER'})`;
        } else if (fieldName === "TENANT_SIG_NAMES") {
            const sigLine = document.querySelector(".sig-block:last-child .sig-line");
            if (sigLine) sigLine.textContent = `(${value || 'TENANT'})`;
        }
    };

    // Number to words conversion (Indian Numbering System)
    const numberToWords = (numStr) => {
        const clean = numStr.replace(/,/g, "").trim();
        const num = parseInt(clean, 10);
        if (isNaN(num)) return "";
        if (num === 0) return "Zero";

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

        // Crores (1,00,00,000)
        if (temp >= 10000000) {
            str += convertLessThanThousand(Math.floor(temp / 10000000)) + " Crore ";
            temp %= 10000000;
        }
        // Lakhs (1,00,000)
        if (temp >= 100000) {
            str += convertLessThanThousand(Math.floor(temp / 100000)) + " Lakh ";
            temp %= 100000;
        }
        // Thousands (1,000)
        if (temp >= 1000) {
            str += convertLessThanThousand(Math.floor(temp / 1000)) + " Thousand ";
            temp %= 1000;
        }
        // Remaining
        if (temp > 0) {
            str += convertLessThanThousand(temp);
        }

        return str.trim();
    };

    // Auto-compute words for Rent and Deposit amounts
    const setupAutoCalculations = () => {
        agreementForm.addEventListener("input", (e) => {
            const fieldId = e.target.id;
            
            if (fieldId === "RENT_AMOUNT") {
                const wordsField = document.getElementById("RENT_AMOUNT_WORDS");
                if (wordsField) {
                    const words = numberToWords(e.target.value);
                    wordsField.value = words;
                    updatePreviewHighlight("RENT_AMOUNT_WORDS", words);
                }
            } else if (fieldId === "DEPOSIT_AMOUNT") {
                const wordsField = document.getElementById("DEPOSIT_AMOUNT_WORDS");
                if (wordsField) {
                    const words = numberToWords(e.target.value);
                    wordsField.value = words;
                    updatePreviewHighlight("DEPOSIT_AMOUNT_WORDS", words);
                }
            } else if (fieldId === "LEASE_PERIOD_NUM") {
                // Keep lease period and lease period num consistent in terms of month numbers
                const periodText = document.getElementById("LEASE_PERIOD");
                if (periodText && e.target.value === "11") {
                    periodText.value = "eleven months";
                    updatePreviewHighlight("LEASE_PERIOD", "eleven months");
                }
            }
        });
    };

    // Fetch field structure and render form
    const loadFields = async () => {
        try {
            const res = await fetch("/api/fields");
            if (!res.ok) throw new Error("Failed to fetch template fields configuration.");
            
            const categories = await res.json();
            formCategories.innerHTML = ""; // Clear loader
            
            for (const [catKey, catVal] of Object.entries(categories)) {
                // Render category card
                const catCard = document.createElement("div");
                catCard.className = "form-category-card";
                
                const catTitle = document.createElement("div");
                catTitle.className = "category-title";
                catTitle.textContent = catVal.title;
                catCard.appendChild(catTitle);
                
                // Render inputs
                for (const [fieldKey, fieldVal] of Object.entries(catVal.fields)) {
                    const group = document.createElement("div");
                    group.className = "form-group";
                    
                    const label = document.createElement("label");
                    label.setAttribute("for", fieldKey);
                    label.textContent = fieldVal.label;
                    group.appendChild(label);
                    
                    let input;
                    if (fieldVal.type === "textarea") {
                        input = document.createElement("textarea");
                    } else {
                        input = document.createElement("input");
                        input.type = fieldVal.type;
                    }
                    
                    input.className = "form-control";
                    input.id = fieldKey;
                    input.name = fieldKey;
                    input.value = fieldVal.default;
                    input.placeholder = fieldVal.placeholder || "";
                    input.required = true;
                    
                    // Input event listener to update preview text in real-time
                    input.addEventListener("input", (e) => {
                        updatePreviewHighlight(fieldKey, e.target.value);
                    });
                    
                    group.appendChild(input);
                    catCard.appendChild(group);
                    
                    // Initialize current fields map
                    currentFields[fieldKey] = fieldVal.default;
                    // Seed initial preview highlight
                    updatePreviewHighlight(fieldKey, fieldVal.default);
                }
                
                formCategories.appendChild(catCard);
            }
            
            setupAutoCalculations();
            
        } catch (error) {
            console.error(error);
            formCategories.innerHTML = `
                <div class="form-loading" style="color: #ef4444;">
                    <i class="fa-solid fa-triangle-exclamation spinner-large"></i>
                    <h3>Error Loading Configuration</h3>
                    <p>${error.message}</p>
                </div>
            `;
        }
    };

    // View Switching logic
    const switchView = (viewType) => {
        if (viewType === "draft") {
            toggleDraftBtn.classList.add("active");
            togglePdfBtn.classList.remove("active");
            draftView.classList.add("active");
            pdfView.classList.remove("active");
        } else if (viewType === "pdf") {
            toggleDraftBtn.classList.remove("active");
            togglePdfBtn.classList.add("active");
            draftView.classList.remove("active");
            pdfView.classList.add("active");
        }
    };

    toggleDraftBtn.addEventListener("click", () => switchView("draft"));
    togglePdfBtn.addEventListener("click", () => switchView("pdf"));

    // Document Generation API Call
    generateBtn.addEventListener("click", async () => {
        if (isGenerating) return;
        
        // Gather values
        const payload = {};
        const formData = new FormData(agreementForm);
        let hasEmptyFields = false;
        
        for (const [key, val] of formData.entries()) {
            if (!val.trim()) {
                hasEmptyFields = true;
            }
            payload[key] = val;
        }

        if (hasEmptyFields) {
            showToast("Please fill in all fields before generating document.");
            return;
        }

        // Set loading state
        isGenerating = true;
        btnSpinner.classList.remove("hide");
        generateBtn.disabled = true;
        
        // Show loading screen over PDF view and switch tabs
        switchView("pdf");
        pdfLoading.classList.remove("hide");
        pdfIframe.src = ""; // Clear previous source
        
        // Disable actions until done
        printBtn.disabled = true;
        downloadDocxBtn.removeAttribute("href");
        downloadDocxBtn.classList.add("disabled");
        downloadDocxBtn.setAttribute("disabled", "true");
        downloadPdfBtn.removeAttribute("href");
        downloadPdfBtn.classList.add("disabled");
        downloadPdfBtn.setAttribute("disabled", "true");

        try {
            const response = await fetch("/api/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errDetail = await response.json();
                throw new Error(errDetail.detail || "Server error during document generation.");
            }

            const result = await response.json();
            
            // Reload PDF Iframe (append timestamp to bypass cache)
            const timestamp = new Date().getTime();
            pdfIframe.src = `${result.pdfUrl}?t=${timestamp}`;
            
            // Hide loading overlay and enable controls immediately (unreliable to wait for onload on PDF iframes)
            pdfLoading.classList.add("hide");
            printBtn.disabled = false;
            
            // Configure Download links
            downloadDocxBtn.href = result.docxUrl;
            downloadDocxBtn.classList.remove("disabled");
            downloadDocxBtn.removeAttribute("disabled");
            
            downloadPdfBtn.href = result.pdfUrl;
            downloadPdfBtn.classList.remove("disabled");
            downloadPdfBtn.removeAttribute("disabled");
            
            togglePdfBtn.disabled = false;
            showToast("Rental Agreement generated successfully!");

        } catch (error) {
            console.error("Generation failed:", error);
            showToast(`Error: ${error.message}`);
            pdfLoading.classList.add("hide");
            switchView("draft");
        } finally {
            isGenerating = false;
            btnSpinner.classList.add("hide");
            generateBtn.disabled = false;
        }
    });

    // Print Handling
    printBtn.addEventListener("click", () => {
        // PDF embeds can sometimes be tricky to print directly via iframe window print
        // across all browsers due to security blocks or PDF reader components.
        // A robust approach is to print the iframe, or open in new window and print.
        try {
            if (pdfIframe && pdfIframe.contentWindow) {
                pdfIframe.contentWindow.focus();
                pdfIframe.contentWindow.print();
            } else {
                throw new Error("Iframe window not accessible");
            }
        } catch (e) {
            // Fallback: Open in new tab which will load native PDF viewer print
            const printWindow = window.open("/api/download/pdf", "_blank");
            if (printWindow) {
                printWindow.onload = () => {
                    printWindow.print();
                };
            } else {
                showToast("Pop-up blocked. Please enable popups or download the PDF to print.");
            }
        }
    });

    // Prevent accidental page reloads on pressing Enter in input fields
    agreementForm.addEventListener("submit", (e) => {
        e.preventDefault();
        generateBtn.click();
    });

    // Initialize Page
    initTheme();
    loadFields();
});
