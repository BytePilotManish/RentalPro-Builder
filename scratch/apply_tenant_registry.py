import os

file_path = "frontend/src/App.jsx"
if not os.path.exists(file_path):
    print("Error: App.jsx not found")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Normalize line endings to LF for replacement processing
has_crlf = "\r\n" in content
content = content.replace("\r\n", "\n")

# 1. Top Import
target1 = 'import { useState, useEffect, useRef } from "react";'
replacement1 = '''import { useState, useEffect, useRef } from "react";
import TenantRegistry from "./components/TenantRegistry";'''

if target1 in content:
    content = content.replace(target1, replacement1)
    print("1. Top import added successfully")
else:
    print("Warning: Target 1 not found")

# 2. State definitions
target2 = '''  // Custom Templates states
  const [customTemplates, setCustomTemplates] = useState([]);
  const [selectedTemplateId, setSelectedTemplateId] = useState(null);'''

replacement2 = '''  // Custom Templates states
  const [customTemplates, setCustomTemplates] = useState([]);
  const [selectedTemplateId, setSelectedTemplateId] = useState(null);

  // Tenant Registry states
  const [tenantsList, setTenantsList] = useState([]);

  const fetchTenants = async () => {
    if (!authToken) return;
    try {
      const res = await fetch("/api/tenants", {
        headers: { "Authorization": `Bearer ${authToken}` }
      });
      if (res.ok) {
        const data = await res.json();
        setTenantsList(data);
      }
    } catch (err) {
      console.error("Error fetching tenants:", err);
    }
  };'''

if target2 in content:
    content = content.replace(target2, replacement2)
    print("2. State definitions added successfully")
else:
    print("Warning: Target 2 not found")

# 3. useEffect call
target3 = '''      fetchNotifications();
      fetchCustomTemplates();
      setCurrentView("dashboard");'''

replacement3 = '''      fetchNotifications();
      fetchCustomTemplates();
      fetchTenants();
      setCurrentView("dashboard");'''

if target3 in content:
    content = content.replace(target3, replacement3)
    print("3. useEffect call added successfully")
else:
    print("Warning: Target 3 not found")

# 4. Render TenantRegistry under activeSidebarTab === "tenants"
target4 = '''              {activeSidebarTab === "tenants" && (
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
              )}'''

replacement4 = '''              {activeSidebarTab === "tenants" && (
                <TenantRegistry
                  authToken={authToken}
                  showToast={showToast}
                  t={t}
                  tenantsList={tenantsList}
                  setTenantsList={setTenantsList}
                  fetchTenants={fetchTenants}
                />
              )}'''

if target4 in content:
    content = content.replace(target4, replacement4)
    print("4. TenantRegistry rendering added successfully")
else:
    target4_alt = target4.replace("text-slate-850", "text-slate-855")
    if target4_alt in content:
        content = content.replace(target4_alt, replacement4)
        print("4. TenantRegistry rendering (alt) added successfully")
    else:
        print("Warning: Target 4 not found")

# 5. Connect saved tenants select dropdown inside customizer
target5 = '''                      <h3 className="text-[11px] font-extrabold text-emerald-700 uppercase tracking-widest border-b border-slate-200 pb-2 mb-3 dark:text-emerald-500 dark:border-slate-800">
                        {category.title}
                      </h3>'''

replacement5 = '''                      <h3 className="text-[11px] font-extrabold text-emerald-700 uppercase tracking-widest border-b border-slate-200 pb-2 mb-3 dark:text-emerald-500 dark:border-slate-800 flex justify-between items-center">
                        <span>{category.title}</span>
                        {(catKey === "TENANT" || catKey === "CUSTOM_FIELDS") && tenantsList.length > 0 && (
                          <select
                            onChange={(e) => {
                              const selectedId = e.target.value;
                              if (!selectedId) return;
                              const tenant = tenantsList.find(t => t.id === parseInt(selectedId, 10));
                              if (tenant) {
                                setFormData(prev => ({
                                  ...prev,
                                  TENANT_NAME: tenant.name || "",
                                  TENANT_PARENT: tenant.guardian || "",
                                  TENANT_AGE: tenant.age ? tenant.age.toString() : "",
                                  TENANT_ADDRESS: tenant.address || "",
                                  TENANT_SIG_NAMES: tenant.name || ""
                                }));
                                showToast(`Filled details for tenant "${tenant.name}"!`, "success");
                              }
                              e.target.value = "";
                            }}
                            className="bg-white border border-slate-250 text-slate-800 text-[10px] font-bold rounded-lg px-2 py-1 outline-none dark:bg-slate-950/60 dark:border-slate-800 dark:text-slate-200 cursor-pointer"
                          >
                            <option value="">👤 Fill from Registry</option>
                            {tenantsList.map(t => (
                              <option key={t.id} value={t.id}>{t.name}</option>
                            ))}
                          </select>
                        )}
                      </h3>'''

if target5 in content:
    content = content.replace(target5, replacement5)
    print("5. Tenant quick fill dropdown added successfully")
else:
    print("Warning: Target 5 not found")

# 6. Modal Nesting Fix
target6 = '''            </div>
          </div>
        </div>
      {/* Create Template Modal */}'''

replacement6 = '''            </div>
          </div>
        </div>
      )}

      {/* Create Template Modal */}'''

if target6 in content:
    content = content.replace(target6, replacement6)
    print("6. Modal nesting start fix applied successfully")
else:
    print("Warning: Target 6 not found")

# 7. Modal Nesting End Fix (remove duplicate `)}`)
target7 = '''      )}
      )}
    </div>
  );
}'''

replacement7 = '''      )}
    </div>
  );
}'''

if target7 in content:
    content = content.replace(target7, replacement7)
    print("7. Modal nesting end duplicate removed successfully")
else:
    print("Warning: Target 7 not found")

# Restore line endings to CRLF if file originally had it
if has_crlf:
    content = content.replace("\n", "\r\n")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("App.jsx modified successfully!")
