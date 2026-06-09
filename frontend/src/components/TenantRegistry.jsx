import { useState, useEffect } from "react";
import { Plus, Trash2, Edit2, Search, User, Mail, Phone, Loader2, FileSignature, CheckCircle } from "lucide-react";

export default function TenantRegistry({
  authToken,
  showToast,
  t,
  tenantsList,
  setTenantsList,
  fetchTenants
}) {
  const [searchQuery, setSearchQuery] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  
  // Form state
  const [tenantId, setTenantId] = useState(null);
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [guardian, setGuardian] = useState("");
  const [age, setAge] = useState("");
  const [address, setAddress] = useState("");
  const [aadhar, setAadhar] = useState("");

  useEffect(() => {
    fetchTenants();
  }, [authToken]);

  const handleOpenAddModal = () => {
    setTenantId(null);
    setName("");
    setPhone("");
    setEmail("");
    setGuardian("");
    setAge("");
    setAddress("");
    setAadhar("");
    setShowModal(true);
  };

  const handleOpenEditModal = (tenant) => {
    setTenantId(tenant.id);
    setName(tenant.name || "");
    setPhone(tenant.phone || "");
    setEmail(tenant.email || "");
    setGuardian(tenant.guardian || "");
    setAge(tenant.age || "");
    setAddress(tenant.address || "");
    setAadhar(tenant.aadhar || "");
    setShowModal(true);
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to remove tenant "${name}" from the registry?`)) return;
    try {
      const res = await fetch(`/api/tenants/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${authToken}` }
      });
      if (res.ok) {
        showToast("Tenant deleted successfully.", "success");
        fetchTenants();
      } else {
        const err = await res.json();
        showToast(err.detail || "Failed to delete tenant", "error");
      }
    } catch (err) {
      showToast(err.message, "error");
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      showToast("Tenant Name is required.", "error");
      return;
    }

    setIsSaving(true);
    const payload = {
      name: name.trim(),
      phone: phone.trim() || null,
      email: email.trim() || null,
      guardian: guardian.trim() || null,
      age: age ? parseInt(age, 10) : null,
      address: address.trim() || null,
      aadhar: aadhar.trim() || null
    };

    const url = tenantId ? `/api/tenants/${tenantId}` : "/api/tenants";
    const method = tenantId ? "PUT" : "POST";

    try {
      const res = await fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${authToken}`
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        showToast(tenantId ? "Tenant updated successfully!" : "Tenant registered successfully!", "success");
        setShowModal(false);
        fetchTenants();
      } else {
        const err = await res.json();
        showToast(err.detail || "Failed to save tenant", "error");
      }
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setIsSaving(false);
    }
  };

  // Filter tenants based on search query
  const filteredTenants = tenantsList.filter(t => 
    (t.name || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (t.phone || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (t.email || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (t.aadhar || "").toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6 text-left">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">Tenant Registry</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Manage tenant database records and link profiles to agreements dynamically.</p>
        </div>
        <button 
          onClick={handleOpenAddModal}
          className="flex items-center gap-2 bg-[#0f9770] hover:bg-[#0d8563] text-white text-xs font-bold px-4 py-2.5 rounded-xl transition-all shadow-md active:scale-95 cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          Add New Tenant
        </button>
      </div>

      {/* Search Bar */}
      <div className="relative max-w-md">
        <span className="absolute inset-y-0 left-0 flex items-center pl-3.5 pointer-events-none text-slate-400">
          <Search className="w-4 h-4" />
        </span>
        <input 
          type="text" 
          placeholder="Search tenants by name, phone, email, aadhar..." 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full bg-white border border-slate-200 focus:border-[#0f9770] focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-xs rounded-xl pl-10 pr-4 py-2.5 outline-none transition-all dark:bg-slate-900/60 dark:border-slate-800 dark:focus:bg-slate-900 dark:text-slate-200"
        />
      </div>

      {/* Tenants Table */}
      <div className="bg-white border border-slate-200 rounded-3xl dark:bg-slate-900/40 dark:border-slate-800 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/20 text-slate-400 text-[10px] font-extrabold uppercase tracking-wider">
                <th className="px-6 py-4 text-left">Tenant Info</th>
                <th className="px-6 py-4 text-left">Contact Details</th>
                <th className="px-6 py-4 text-left">Guardian & Age</th>
                <th className="px-6 py-4 text-left">Address</th>
                <th className="px-6 py-4 text-left">Aadhar Status</th>
                <th className="px-6 py-4 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-350">
              {filteredTenants.length === 0 ? (
                <tr>
                  <td colSpan="6" className="text-center py-10 text-slate-400 dark:text-slate-550">
                    No tenants registered in database matching query. Click "Add New Tenant" to create one.
                  </td>
                </tr>
              ) : (
                filteredTenants.map((tenant) => (
                  <tr key={tenant.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-900/30">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2.5">
                        <div className="p-2 bg-emerald-500/10 rounded-xl text-emerald-600 dark:bg-emerald-500/15 dark:text-emerald-400">
                          <User className="w-4 h-4" />
                        </div>
                        <div>
                          <p className="font-bold text-slate-800 dark:text-white text-[13px]">{tenant.name}</p>
                          <p className="text-[10px] text-slate-400 dark:text-slate-500">ID: #{tenant.id}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1">
                        {tenant.phone && (
                          <span className="flex items-center gap-1.5 text-slate-600 dark:text-slate-300">
                            <Phone className="w-3 h-3 text-slate-400" />
                            {tenant.phone}
                          </span>
                        )}
                        {tenant.email && (
                          <span className="flex items-center gap-1.5 text-slate-600 dark:text-slate-300">
                            <Mail className="w-3 h-3 text-slate-400" />
                            {tenant.email}
                          </span>
                        )}
                        {!tenant.phone && !tenant.email && (
                          <span className="text-slate-400 italic">No contact info</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-slate-700 dark:text-slate-200">{tenant.guardian || "Not Set"}</p>
                        <p className="text-[10px] text-slate-400 mt-0.5">Age: {tenant.age || "N/A"}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 max-w-xs truncate" title={tenant.address}>
                      {tenant.address || "Not Set"}
                    </td>
                    <td className="px-6 py-4">
                      {tenant.aadhar ? (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-400 border border-emerald-200/40">
                          <CheckCircle className="w-3 h-3 text-emerald-500" />
                          Aadhar Linked
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold bg-slate-50 text-slate-500 dark:bg-slate-900/50 dark:text-slate-400 border border-slate-200/40">
                          Not Provided
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center items-center gap-2">
                        <button
                          onClick={() => handleOpenEditModal(tenant)}
                          className="p-1.5 text-slate-400 hover:text-emerald-600 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg transition-all cursor-pointer"
                          title="Edit Tenant"
                        >
                          <Edit2 className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleDelete(tenant.id, tenant.name)}
                          className="p-1.5 text-slate-400 hover:text-rose-500 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg transition-all cursor-pointer"
                          title="Delete Tenant"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add / Edit Tenant Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm dark:bg-slate-950/80 transition-all duration-300 overflow-y-auto">
          <div className="bg-white border border-slate-200/80 dark:bg-slate-900 dark:border-slate-800 rounded-3xl w-full max-w-lg p-6 shadow-2xl space-y-5 transform transition-all scale-100 duration-200 text-left my-8">
            <div className="flex justify-between items-center border-b pb-3 border-slate-100 dark:border-slate-800">
              <h3 className="text-base font-extrabold text-slate-850 dark:text-white flex items-center gap-2">
                <FileSignature className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                {tenantId ? "Edit Tenant Profile" : "Register New Tenant"}
              </h3>
              <button 
                type="button"
                onClick={() => setShowModal(false)}
                className="text-slate-400 hover:text-slate-655 dark:text-slate-500 dark:hover:text-slate-300 text-sm font-bold cursor-pointer"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSave} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                    placeholder="e.g. Mr. RAJUGOWDA"
                    required
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                    placeholder="e.g. +91 9988776655"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                    placeholder="e.g. rajugowda@gmail.com"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                    Tenant Age
                  </label>
                  <input
                    type="number"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                    placeholder="e.g. 47"
                  />
                </div>
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Parent / Guardian / Spouse (S/O, D/O, W/O)
                </label>
                <input
                  type="text"
                  value={guardian}
                  onChange={(e) => setGuardian(e.target.value)}
                  className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                  placeholder="e.g. S/O Subbegowda"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Aadhar Number / Reference ID
                </label>
                <input
                  type="text"
                  value={aadhar}
                  onChange={(e) => setAadhar(e.target.value)}
                  className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                  placeholder="e.g. 12-digit Aadhar card number"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Residential Address
                </label>
                <textarea
                  rows={3}
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all resize-none dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                  placeholder="No. 18, 3rd Cross, Rajeev Gandhi Nagar, Laggere, Bengaluru-560 058"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-100 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 border border-slate-200/80 hover:border-slate-350 text-xs font-bold rounded-xl text-slate-500 hover:text-slate-800 bg-white transition-all dark:border-slate-800 dark:bg-slate-950 dark:text-slate-400 dark:hover:text-white cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSaving}
                  className="flex items-center gap-1.5 bg-[#0f9770] hover:bg-[#0d8563] text-white text-xs font-bold px-5 py-2.5 rounded-xl shadow-md transition-all active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                >
                  {isSaving && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                  Save Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
