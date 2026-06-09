import { useState, useEffect } from "react";
import { Plus, Trash2, Edit2, Search, Building, Loader2, FileSignature, MapPin } from "lucide-react";

export default function PropertyRegistry({
  authToken,
  showToast,
  t,
  propertiesList,
  setPropertiesList,
  fetchProperties
}) {
  const [searchQuery, setSearchQuery] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  
  // Form state
  const [propertyId, setPropertyId] = useState(null);
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [description, setDescription] = useState("");
  const [businessName, setBusinessName] = useState("");

  useEffect(() => {
    fetchProperties();
  }, [authToken]);

  const handleOpenAddModal = () => {
    setPropertyId(null);
    setName("");
    setAddress("");
    setDescription("");
    setBusinessName("");
    setShowModal(true);
  };

  const handleOpenEditModal = (prop) => {
    setPropertyId(prop.id);
    setName(prop.name || "");
    setAddress(prop.address || "");
    setDescription(prop.description || "");
    setBusinessName(prop.business_name || "");
    setShowModal(true);
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to delete property "${name}"?`)) return;
    try {
      const res = await fetch(`/api/properties/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${authToken}` }
      });
      if (res.ok) {
        showToast("Property deleted successfully.", "success");
        fetchProperties();
      } else {
        const err = await res.json();
        showToast(err.detail || "Failed to delete property", "error");
      }
    } catch (err) {
      showToast(err.message, "error");
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      showToast("Property Name is required.", "error");
      return;
    }
    if (!address.trim()) {
      showToast("Property Address is required.", "error");
      return;
    }

    setIsSaving(true);
    const payload = {
      name: name.trim(),
      address: address.trim(),
      description: description.trim() || null,
      business_name: businessName.trim() || null
    };

    const url = propertyId ? `/api/properties/${propertyId}` : "/api/properties";
    const method = propertyId ? "PUT" : "POST";

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
        showToast(propertyId ? "Property updated successfully!" : "Property registered successfully!", "success");
        setShowModal(false);
        fetchProperties();
      } else {
        const err = await res.json();
        showToast(err.detail || "Failed to save property", "error");
      }
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setIsSaving(false);
    }
  };

  // Filter properties based on search query
  const filteredProperties = propertiesList.filter(p => 
    (p.name || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (p.address || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (p.business_name || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (p.description || "").toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6 text-left">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-slate-850 dark:text-white tracking-tight">Property Assets Directory</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Track rental premises, retail spaces, and commercial building amenities.</p>
        </div>
        <button 
          onClick={handleOpenAddModal}
          className="flex items-center gap-2 bg-[#0f9770] hover:bg-[#0d8563] text-white text-xs font-bold px-4 py-2.5 rounded-xl transition-all shadow-md active:scale-95 cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          Add New Property
        </button>
      </div>

      {/* Search Bar */}
      <div className="relative max-w-md">
        <span className="absolute inset-y-0 left-0 flex items-center pl-3.5 pointer-events-none text-slate-400">
          <Search className="w-4 h-4" />
        </span>
        <input 
          type="text" 
          placeholder="Search properties by name, address, business..." 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full bg-white border border-slate-200 focus:border-[#0f9770] focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-xs rounded-xl pl-10 pr-4 py-2.5 outline-none transition-all dark:bg-slate-900/60 dark:border-slate-800 dark:focus:bg-slate-900 dark:text-slate-200"
        />
      </div>

      {/* Properties Table */}
      <div className="bg-white border border-slate-200 rounded-3xl dark:bg-slate-900/40 dark:border-slate-800 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/20 text-slate-400 text-[10px] font-extrabold uppercase tracking-wider">
                <th className="px-6 py-4 text-left">Property Name</th>
                <th className="px-6 py-4 text-left">Business Outlet</th>
                <th className="px-6 py-4 text-left">Premises Address</th>
                <th className="px-6 py-4 text-left">Amenities & Description</th>
                <th className="px-6 py-4 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-350">
              {filteredProperties.length === 0 ? (
                <tr>
                  <td colSpan="5" className="text-center py-10 text-slate-400 dark:text-slate-550">
                    No properties registered in database matching query. Click "Add New Property" to create one.
                  </td>
                </tr>
              ) : (
                filteredProperties.map((prop) => (
                  <tr key={prop.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-900/30">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2.5">
                        <div className="p-2 bg-emerald-500/10 rounded-xl text-emerald-600 dark:bg-emerald-500/15 dark:text-emerald-400">
                          <Building className="w-4 h-4" />
                        </div>
                        <div>
                          <p className="font-bold text-slate-800 dark:text-white text-[13px]">{prop.name}</p>
                          <p className="text-[10px] text-slate-400 dark:text-slate-500">ID: #{prop.id}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center gap-1 text-slate-700 dark:text-slate-300 font-bold bg-slate-50 dark:bg-slate-950 px-2 py-1 rounded-lg border dark:border-slate-800">
                        {prop.business_name || "N/A"}
                      </span>
                    </td>
                    <td className="px-6 py-4 max-w-xs truncate" title={prop.address}>
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
                        {prop.address}
                      </span>
                    </td>
                    <td className="px-6 py-4 max-w-sm truncate" title={prop.description}>
                      {prop.description || <span className="text-slate-400 italic">No description</span>}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center items-center gap-2">
                        <button
                          onClick={() => handleOpenEditModal(prop)}
                          className="p-1.5 text-slate-400 hover:text-emerald-600 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg transition-all cursor-pointer"
                          title="Edit Property"
                        >
                          <Edit2 className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleDelete(prop.id, prop.name)}
                          className="p-1.5 text-slate-400 hover:text-rose-500 hover:bg-slate-50 dark:hover:bg-slate-800 rounded-lg transition-all cursor-pointer"
                          title="Delete Property"
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

      {/* Add / Edit Property Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm dark:bg-slate-950/80 transition-all duration-300 overflow-y-auto">
          <div className="bg-white border border-slate-200/80 dark:bg-slate-900 dark:border-slate-800 rounded-3xl w-full max-w-lg p-6 shadow-2xl space-y-5 transform transition-all scale-100 duration-200 text-left my-8">
            <div className="flex justify-between items-center border-b pb-3 border-slate-100 dark:border-slate-800">
              <h3 className="text-base font-extrabold text-slate-855 dark:text-white flex items-center gap-2">
                <FileSignature className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                {propertyId ? "Edit Property Asset" : "Register Property Asset"}
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
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Property Display Name *
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                  placeholder="e.g. Laggere Commercial Shop"
                  required
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Business Outlet Name
                </label>
                <input
                  type="text"
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-800 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                  placeholder="e.g. J S TRADERS"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Premises Full Address *
                </label>
                <textarea
                  rows={3}
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-855 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all resize-none dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                  placeholder="e.g. No.99 & 100C, Near Sri Kalikamba Temple Chowdeshwari Nagar, Laggere, Bengaluru- 560 058"
                  required
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Amenities & Description
                </label>
                <textarea
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="bg-slate-50 border border-slate-200/80 focus:border-emerald-500 focus:bg-white focus:ring-4 focus:ring-emerald-500/10 text-slate-855 text-sm rounded-xl px-3.5 py-2.5 outline-none transition-all resize-none dark:bg-slate-950/60 dark:border-slate-800 dark:focus:bg-slate-950 dark:text-slate-200"
                  placeholder="e.g. One RCC Roofed Shops, with rolling Shutter and electricity, Toilet and water facility"
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
                  Save Property
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
