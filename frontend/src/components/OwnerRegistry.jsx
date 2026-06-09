import { useState, useEffect } from "react";
import { Plus, Trash2, Edit2, Search, User, Mail, Phone, Loader2, FileSignature, Landmark } from "lucide-react";

export default function OwnerRegistry({
  authToken,
  showToast,
  t,
  ownersList,
  setOwnersList,
  fetchOwners
}) {
  const [searchQuery, setSearchQuery] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  
  // Form state
  const [ownerId, setOwnerId] = useState(null);
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [guardian, setGuardian] = useState("");
  const [age, setAge] = useState("");
  const [address, setAddress] = useState("");

  useEffect(() => {
    fetchOwners();
  }, [authToken]);

  const handleOpenAddModal = () => {
    setOwnerId(null);
    setName("");
    setPhone("");
    setEmail("");
    setGuardian("");
    setAge("");
    setAddress("");
    setShowModal(true);
  };

  const handleOpenEditModal = (owner) => {
    setOwnerId(owner.id);
    setName(owner.name || "");
    setPhone(owner.phone || "");
    setEmail(owner.email || "");
    setGuardian(owner.guardian || "");
    setAge(owner.age || "");
    setAddress(owner.address || "");
    setShowModal(true);
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to remove owner "${name}" from the registry?`)) return;
    try {
      const res = await fetch(`/api/owners/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${authToken}` }
      });
      if (res.ok) {
        showToast("Owner deleted successfully.", "success");
        fetchOwners();
      } else {
        const err = await res.json();
        showToast(err.detail || "Failed to delete owner", "error");
      }
    } catch (err) {
      showToast(err.message, "error");
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      showToast("Owner Name is required.", "error");
      return;
    }

    setIsSaving(true);
    const payload = {
      name: name.trim(),
      phone: phone.trim() || null,
      email: email.trim() || null,
      guardian: guardian.trim() || null,
      age: age ? parseInt(age, 10) : null,
      address: address.trim() || null
    };

    const url = ownerId ? `/api/owners/${ownerId}` : "/api/owners";
    const method = ownerId ? "PUT" : "POST";

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
        showToast(ownerId ? "Owner updated successfully!" : "Owner registered successfully!", "success");
        setShowModal(false);
        fetchOwners();
      } else {
        const err = await res.json();
        showToast(err.detail || "Failed to save owner", "error");
      }
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setIsSaving(false);
    }
  };

  // Filter owners based on search query
  const filteredOwners = ownersList.filter(o => 
    (o.name || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (o.phone || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (o.email || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (o.address || "").toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6 text-left">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">Owners Registry</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Manage landlord database records and link profiles to agreements dynamically.</p>
        </div>
        <button 
          onClick={handleOpenAddModal}
          className="flex items-center gap-2 bg-[#0f9770] hover:bg-[#0d8563] text-white text-xs font-bold px-4 py-2.5 rounded-xl transition-all shadow-md active:scale-95 cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          Add New Owner
        </button>
      </div>

      {/* Search Bar */}
      <div className="relative max-w-md">
        <span className="absolute inset-y-0 left-0 flex items-center pl-3.5 pointer-events-none text-slate-400">
          <Search className="w-4 h-4" />
        </span>
        <input 
          type="text" 
          placeholder="Search owners by name, phone, email..." 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full bg-white border border-slate-200 focus:border-[#0f9770] focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-xs rounded-xl pl-10 pr-4 py-2.5 outline-none transition-all dark:bg-slate-900/60 dark:border-slate-800 dark:focus:bg-slate-900 dark:text-slate-200"
        />
      </div>

      {/* Owners Table */}
      <div className="bg-white border border-slate-200 rounded-3xl dark:bg-slate-900/40 dark:border-slate-800 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/20 text-slate-400 text-[10px] font-extrabold uppercase tracking-wider">
                <th className="px-6 py-4 text-left">Owner Info</th>
                <th className="px-6 py-4 text-left">Contact Details</th>
                <th className="px-6 py-4 text-left">Guardian & Age</th>
                <th className="px-6 py-4 text-left">Registered Address</th>
                <th className="px-6 py-4 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-350">
              {filteredOwners.length === 0 ? (
                <tr>
                  <td colSpan="5" className="text-center py-10 text-slate-400 dark:text-slate-550">
                    No owners registered in database matching query. Click "Add New Owner" to create one.
                  </td>
                </tr>
              ) : (
                filteredOwners.map((owner) => (
                  <tr key={owner.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-900/30">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2.5">
                        <div className="p-2 bg-emerald-500/10 rounded-xl text-emerald-600 dark:bg-emerald-500/15 dark:text-emerald-400">
                          <User className="w-4 h-4" />
                        </div>
                        <div>
                          <p className="font-bold text-slate-800 dark:text-white text-[13px]">{owner.name}</p>
                          <p className="text-[10px] text-slate-400 dark:text-slate-500">ID: #{owner.id}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1">
                        {owner.phone && (
                          <span className="flex items-center gap-1.5 text-slate-600 dark:text-slate-300">
                            <Phone className="w-3 h-3 text-slate-400" />
                            {owner.phone}
                          </span>
                        )}
                        {owner.email && (
                          <span className="flex items-center gap-1.5 text-slate-600 dark:text-slate-300">
                            <Mail className="w-3 h-3 text-slate-400" />
                            {owner.email}
                          </span>
                        )}
                        {!owner.phone && !owner.email && (
                          <span className="text-slate-400 italic">No contact info</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div>
                        <p className="text-slate-700 dark:text-slate-200">{owner.guardian || "Not Set"}</p>
                        <p className="text-[10px] text-slate-400 mt-0.5">Age: {owner.age || "N/A"}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 max-w-xs truncate" title={owner.address}>
                      {owner.address || "Not Set"}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center items-center gap-2">
                        <button
                          onClick={() => handleOpenEditModal(owner)}
                          className="p-1.5 text-slate-400 hover:text-emerald-600 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg transition-all cursor-pointer"
                          title="Edit Owner"
                        >
                          <Edit2 className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleDelete(owner.id, owner.name)}
                          className="p-1.5 text-slate-400 hover:text-rose-500 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg transition-all cursor-pointer"
                          title="Delete Owner"
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

      {/* Add / Edit Owner Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm dark:bg-slate-950/80 transition-all duration-300 overflow-y-auto">
          <div className="bg-white border border-slate-200/80 dark:bg-slate-900 dark:border-slate-800 rounded-3xl w-full max-w-lg p-6 shadow-2xl space-y-5 transform transition-all scale-100 duration-200 text-left my-8">
            <div className="flex justify-between items-center border-b pb-3 border-slate-100 dark:border-slate-800">
              <h3 className="text-base font-extrabold text-slate-850 dark:text-white flex items-center gap-2">
                <FileSignature className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                {ownerId ? "Edit Owner Profile" : "Register New Owner"}
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
                    placeholder="e.g. Mr. MANOJ M"
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
                    placeholder="e.g. landlord@example.com"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                    Owner Age
                  </label>
                  <input
                    type="number"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                    placeholder="e.g. 45"
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
                  placeholder="e.g. S/O T Mahesh"
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
                  className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-855 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all resize-none dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                  placeholder="No,99,100 C Near Sri Kalikamba Temple, ChowdeshwariNagar, , Laggere, Bengaluru- 560 058"
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
