import os

file_path = "frontend/src/App.jsx"
if not os.path.exists(file_path):
    print("Error: App.jsx not found")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Ensure Phone is imported from lucide-react in App.jsx
if "Phone" not in content:
    content = content.replace("  User as UserIcon,", "  User as UserIcon,\n  Phone,")
    print("Phone icon added to imports")

# 2. Robust index-based replacement for Login View block
start_header = "      {/* View router: Login */}"
end_header = "      {/* View router: Register */}"

# Normalize line endings to LF for index matching
has_crlf = "\r\n" in content
content_lf = content.replace("\r\n", "\n")

start_idx = content_lf.find(start_header)
end_idx = content_lf.find(end_header)

if start_idx != -1 and end_idx != -1:
    old_block = content_lf[start_idx:end_idx]
    
    replacement_login = """      {/* View router: Login */}
      {currentView === "login" && (
        <div className="min-h-screen flex flex-col md:flex-row bg-slate-50 dark:bg-slate-950 transition-colors duration-250 w-full overflow-hidden">
          
          {/* Left Column: Brand, Feature Showcase, Qryvanta Logo & Customer Support */}
          <div className="w-full md:w-1/2 bg-slate-900 text-white p-8 md:p-12 lg:p-16 flex flex-col justify-between relative overflow-hidden">
            {/* Background pattern/gradient */}
            <div className="absolute inset-0 bg-gradient-to-br from-[#0c5943]/20 via-slate-900 to-indigo-950/40 z-0" />
            <div className="absolute top-[-10%] right-[-10%] w-[300px] h-[300px] rounded-full bg-emerald-500/10 blur-[100px] z-0" />
            <div className="absolute bottom-[-15%] left-[-15%] w-[400px] h-[400px] rounded-full bg-indigo-500/10 blur-[120px] z-0" />

            <div className="relative z-10 flex flex-col h-full justify-between gap-12">
              {/* Header: App Name & Logo */}
              <div className="flex items-center gap-3">
                <div className="p-2.5 bg-emerald-500/15 border border-emerald-500/30 rounded-2xl">
                  <FileSignature className="w-6 h-6 text-emerald-400" />
                </div>
                <span className="text-xl font-black tracking-tight text-white uppercase">{t("brandName") || "RentalPro Builder"}</span>
              </div>

              {/* Main Pitch */}
              <div className="space-y-6 my-auto">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold uppercase tracking-wider">
                  <Sparkles className="w-3.5 h-3.5" /> Next-Gen Agreement Builder
                </div>
                <h2 className="text-3xl lg:text-4xl xl:text-5xl font-black leading-tight text-white">
                  Generate verified rental contracts in seconds.
                </h2>
                <p className="text-base text-slate-400 max-w-md leading-relaxed font-normal">
                  Fast, compliant, and secure document creation. Crafted for professional landlords, property managers, and tenants.
                </p>

                {/* Features Grid */}
                <div className="grid grid-cols-2 gap-6 pt-4">
                  <div className="space-y-1">
                    <h5 className="font-bold text-white text-sm">📄 Instant PDFs</h5>
                    <p className="text-xs text-slate-400">Generate high-fidelity legal templates automatically.</p>
                  </div>
                  <div className="space-y-1">
                    <h5 className="font-bold text-white text-sm">🔒 Cloud Secured</h5>
                    <p className="text-xs text-slate-400">Secure storage with instant access anytime, anywhere.</p>
                  </div>
                </div>
              </div>

              {/* Footer Part in Left Panel (Developer + Support info) */}
              <div className="space-y-6 pt-6 border-t border-slate-800">
                {/* Customer Support */}
                <div className="space-y-3">
                  <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                    <Phone className="w-3.5 h-3.5 text-emerald-400" /> Customer Support
                  </h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-slate-950/50 border border-slate-800/80 p-4 rounded-2xl backdrop-blur-sm">
                    <div className="space-y-1">
                      <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Call Support</span>
                      <div>
                        <a href="tel:+919844328163" className="text-sm font-bold text-white hover:text-emerald-400 transition-colors">
                          +91 9844328163
                        </a>
                      </div>
                    </div>
                    <div className="space-y-1">
                      <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">Email Support</span>
                      <div>
                        <a href="mailto:manishrahul2003@gmail.com" className="text-sm font-bold text-white hover:text-emerald-400 transition-colors truncate block">
                          manishrahul2003@gmail.com
                        </a>
                      </div>
                    </div>
                    <div className="sm:col-span-2 flex items-center gap-3 pt-2 border-t border-slate-800/50 mt-1">
                      <input 
                        type="checkbox" 
                        id="whatsapp-connect-left" 
                        className="w-4 h-4 rounded text-emerald-550 focus:ring-emerald-500 border-slate-700 bg-slate-850 cursor-pointer"
                        onChange={(e) => {
                          if (e.target.checked) {
                            window.open("https://wa.me/919844328163", "_blank");
                            setTimeout(() => {
                              e.target.checked = false;
                            }, 500);
                          }
                        }}
                      />
                      <label htmlFor="whatsapp-connect-left" className="text-xs text-slate-400 cursor-pointer flex items-center justify-between w-full">
                        <span>Connect to WhatsApp for instant chat support</span>
                        <span className="text-[9px] bg-emerald-500/20 text-emerald-400 px-2 py-0.5 rounded-lg font-black uppercase tracking-wider">Chat Now</span>
                      </label>
                    </div>
                  </div>
                </div>

                {/* Developer */}
                <div className="flex items-center justify-between gap-4">
                  <span className="text-xs font-semibold text-slate-500">Made by Qryvanta Technologies</span>
                  <div className="bg-white/95 px-3 py-1.5 rounded-xl border border-slate-800/20 shadow-sm flex items-center justify-center">
                    <img src="/qryvanta_logo.jpg" alt="Qryvanta Technologies" className="h-6 object-contain" />
                  </div>
                </div>
              </div>

            </div>
          </div>

          {/* Right Column: Interactive Login Form */}
          <div className="w-full md:w-1/2 flex items-center justify-center p-8 md:p-12 lg:p-16 relative bg-white dark:bg-slate-950">
            {/* Background blurs for dark/light */}
            <div className="absolute top-[20%] right-[20%] w-[350px] h-[350px] rounded-full bg-indigo-500/5 dark:bg-indigo-500/10 blur-[90px] pointer-events-none z-0" />
            <div className="absolute bottom-[20%] left-[10%] w-[300px] h-[300px] rounded-full bg-emerald-500/5 dark:bg-emerald-500/5 blur-[80px] pointer-events-none z-0" />

            <div className="w-full max-w-md space-y-8 relative z-10">
              <div className="space-y-2.5">
                <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">{t("welcomeBack")}</h1>
                <p className="text-sm text-slate-500 dark:text-slate-400">{t("welcomeSub")}</p>
              </div>

              <form onSubmit={handleLogin} className="space-y-5">
                <div className="space-y-1.5">
                  <label className="text-xs font-extrabold text-slate-500 dark:text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                    <Mail className="w-3.5 h-3.5 text-slate-400" /> {t("emailAddress")}
                  </label>
                  <input
                    type="email"
                    value={loginEmail}
                    onChange={(e) => setLoginEmail(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 rounded-xl px-4 py-3 outline-none transition-all dark:bg-slate-900/60 dark:border-slate-800 dark:focus:bg-slate-900/60 dark:text-slate-200 text-sm shadow-sm"
                    placeholder="e.g. admin@rentalpro.com"
                    required
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-extrabold text-slate-500 dark:text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                    <Lock className="w-3.5 h-3.5 text-slate-400" /> {t("password")}
                  </label>
                  <input
                    type="password"
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 rounded-xl px-4 py-3 outline-none transition-all dark:bg-slate-900/60 dark:border-slate-800 dark:focus:bg-slate-900/60 dark:text-slate-200 text-sm shadow-sm"
                    placeholder="••••••••"
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-[#0f9770] hover:bg-[#0d8563] text-white font-bold py-3.5 rounded-xl shadow-lg shadow-emerald-500/10 hover:shadow-emerald-500/20 active:scale-[0.99] transition-all cursor-pointer text-center text-sm"
                >
                  Log In
                </button>
              </form>

              <div className="space-y-6 pt-4 border-t border-slate-100 dark:border-slate-800">
                <p className="text-sm text-slate-500 dark:text-slate-400">
                  {t("dontHaveAccount")}{" "}
                  <button 
                    onClick={() => setCurrentView("register")}
                    className="text-emerald-600 dark:text-emerald-400 hover:underline font-bold"
                  >
                    {t("signUp")}
                  </button>
                </p>

                <div className="text-[11px] text-slate-500 bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800/60 p-4 rounded-xl leading-relaxed">
                  <span className="font-bold text-slate-700 dark:text-slate-300 block mb-1">🔑 Demo accounts ready for testing:</span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
                    <div className="bg-white dark:bg-slate-950 p-2 rounded border border-slate-100 dark:border-slate-800">
                      <span className="font-bold text-emerald-600 dark:text-emerald-400 block">Administrator</span>
                      admin@rentalpro.com<br/>pw: <span className="font-medium text-slate-700 dark:text-slate-350">admin123</span>
                    </div>
                    <div className="bg-white dark:bg-slate-950 p-2 rounded border border-slate-100 dark:border-slate-800">
                      <span className="font-bold text-emerald-600 dark:text-emerald-400 block">Tenant User</span>
                      tenant@rentalpro.com<br/>pw: <span className="font-medium text-slate-700 dark:text-slate-350">tenant123</span>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

        </div>
      )}
"""
    # Replace the old block
    content_lf = content_lf.replace(old_block, replacement_login)
    print("Success: Login view replaced successfully using robust index lookup!")
else:
    print("Error: Could not locate start or end headers in App.jsx")

if has_crlf:
    content_lf = content_lf.replace("\n", "\r\n")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content_lf)
