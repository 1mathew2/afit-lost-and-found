/* AFIT Lost & Found Portal - front-end logic */

document.getElementById('date').valueAsDate = new Date();

/* ---- Session (sign-in with email) ---- */
let currentUser = null;
try { currentUser = JSON.parse(localStorage.getItem('afit_lf_user') || 'null'); } catch (e) { currentUser = null; }

function renderAuthArea() {
    const area = document.getElementById('authArea');
    if (currentUser) {
        area.innerHTML = `
            <div class="flex items-center gap-2">
                <div class="w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs font-bold" title="${escapeHtml(currentUser.email)}">${escapeHtml((currentUser.name || '?').charAt(0).toUpperCase())}</div>
                <span class="hidden md:inline text-sm font-semibold text-slate-700">${escapeHtml(currentUser.name)}</span>
                <button onclick="signOut()" class="text-xs font-bold text-slate-500 hover:text-rose-600 px-2 py-1.5">Sign out</button>
            </div>`;
    } else {
        area.innerHTML = `<button onclick="openAuthModal('signin')" class="px-3 sm:px-4 py-2 rounded-lg font-semibold text-sm transition border border-slate-300 text-slate-700 hover:bg-slate-50">Sign in</button>`;
    }
}

function openAuthModal(mode) {
    setAuthMode(mode || 'signin');
    document.getElementById('authModal').classList.remove('hidden');
    if (currentUser) {
        document.getElementById('auth_email').value = currentUser.email || '';
    }
}

function setAuthMode(mode) {
    authMode = mode;
    const isSignup = mode === 'signup';
    document.getElementById('authTitle').innerText = isSignup ? 'Create your account' : 'Sign in';
    document.getElementById('authSubmitBtn').innerText = isSignup ? 'Create Account' : 'Sign In';
    document.getElementById('authNameWrap').classList.toggle('hidden', !isSignup);
    document.getElementById('auth_name').required = isSignup;
    const on = 'py-2 rounded-lg text-sm font-bold bg-emerald-600 text-white';
    const off = 'py-2 rounded-lg text-sm font-bold bg-slate-100 text-slate-600';
    document.getElementById('tab-signin').className = isSignup ? off : on;
    document.getElementById('tab-signup').className = isSignup ? on : off;
}

function closeAuthModal() {
    document.getElementById('authModal').classList.add('hidden');
}

let authMode = 'signin';

async function submitAuth(e) {
    e.preventDefault();
    const email = document.getElementById('auth_email').value.trim();
    const password = document.getElementById('auth_password').value;
    const endpoint = authMode === 'signup' ? '/api/signup' : '/api/login';
    const payload = authMode === 'signup'
        ? { name: document.getElementById('auth_name').value.trim(), email: email, password: password }
        : { email: email, password: password };
    const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    if (res.ok) {
        currentUser = await res.json();
        localStorage.setItem('afit_lf_user', JSON.stringify(currentUser));
        closeAuthModal();
        renderAuthArea();
        prefillFromProfile();
    } else {
        let msg = authMode === 'signup' ? 'Sign up failed.' : 'Sign in failed.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

function signOut() {
    currentUser = null;
    localStorage.removeItem('afit_lf_user');
    renderAuthArea();
}

function requireSignIn() {
    if (currentUser) return true;
    openAuthModal('signin');
    return false;
}

function prefillFromProfile() {
    if (!currentUser) return;
    const set = (id, v) => { const el = document.getElementById(id); if (el && !el.value) el.value = v; };
    set('contact_name', currentUser.name);
    set('contact_email', currentUser.email);
    set('claimant_name', currentUser.name);
}

function switchTab(tab) {
    ['browse', 'report', 'guide'].forEach(t => {
        const el = document.getElementById(`section-${t}`);
        const btn = document.getElementById(`btn-${t}`);
        if (t === tab) {
            if (el) el.classList.remove('hidden');
            if (btn) btn.className = 'px-3 sm:px-4 py-2 rounded-lg font-semibold text-sm transition bg-emerald-600 text-white' + (t === 'guide' ? ' flex items-center' : '');
        } else {
            if (el) el.classList.add('hidden');
            if (btn) btn.className = 'px-3 sm:px-4 py-2 rounded-lg font-semibold text-sm transition text-slate-600 hover:text-slate-900 hover:bg-slate-100' + (t === 'guide' ? ' hidden sm:flex items-center' : '');
        }
    });
    if (tab === 'browse') loadItems();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function setHeroType(val) {
    document.getElementById('filterType').value = val;
    loadItems();
}

let itemsCache = {};
let unreadCounts = {};
let readCounts = {};
try { readCounts = JSON.parse(localStorage.getItem('afit_lf_read') || '{}'); } catch (e) { readCounts = {}; }

function saveReadCounts() {
    localStorage.setItem('afit_lf_read', JSON.stringify(readCounts));
}

async function fetchUnreadCounts() {
    if (!currentUser) { unreadCounts = {}; return; }
    try {
        const r = await fetch(`/api/chat/unread?user_email=${encodeURIComponent(currentUser.email)}`);
        if (r.ok) unreadCounts = await r.json();
    } catch (e) {}
}

async function loadItems() {
    const type = document.getElementById('filterType').value;
    const category = document.getElementById('filterCategory').value;
    const location = document.getElementById('filterLocation').value;
    const search = document.getElementById('searchInput').value;

    let url = '/api/items?';
    if (type) url += `item_type=${type}&`;
    if (category) url += `category=${encodeURIComponent(category)}&`;
    if (location) url += `location=${encodeURIComponent(location)}&`;
    if (search) url += `search=${encodeURIComponent(search)}`;
    if (currentUser) url += `viewer_email=${encodeURIComponent(currentUser.email)}`;

    const res = await fetch(url);
    const items = await res.json();
    await fetchUnreadCounts();
    itemsCache = {};
    items.forEach(i => { itemsCache[i.id] = i; });

    document.getElementById('stat-total').innerText = items.length;
    document.getElementById('stat-active').innerText = items.filter(i => i.status === 'Active').length;

    const grid = document.getElementById('itemsGrid');
    grid.innerHTML = '';

    if (items.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full bg-white rounded-2xl p-16 text-center border border-slate-200 shadow-sm space-y-2">
                <h3 class="text-xl font-bold text-slate-800">No matching AFIT property found</h3>
                <p class="text-sm text-slate-500">Try adjusting your search query, category filter, or report a missing item.</p>
            </div>`;
        return;
    }

    items.forEach(item => {
        const isLost = item.item_type === 'lost';
        const badgeBg = isLost ? 'bg-rose-50 text-rose-700 border-rose-200' : 'bg-emerald-50 text-emerald-700 border-emerald-200';
        const statusStyles = {
            'Active': 'bg-amber-50 text-amber-700 border-amber-200',
            'Claim Requested': 'bg-blue-50 text-blue-700 border-blue-200',
            'Claimed/Returned': 'bg-emerald-50 text-emerald-700 border-emerald-200',
            'Closed': 'bg-slate-100 text-slate-600 border-slate-200'
        };
        const statusBg = statusStyles[item.status] || 'bg-slate-100 text-slate-600 border-slate-200';
        const custodyNote = item.custody === 'finder' ? 'With the finder' : (item.custody === 'security' ? 'At security post' : '');
        const titleAttr = escapeHtml(item.title).replace(/'/g, "\\'");
        const isMyReport = !!item.viewer_is_reporter;
        const isMyClaim = !!item.viewer_is_claimant;
        const myFoundReport = !!item.viewer_is_finder;
        const isRejectedClaimant = currentUser && (item.rejected_claimants || []).map(e => String(e).toLowerCase()).includes(currentUser.email.toLowerCase());
        const disputeCount = (item.disputes || []).filter(d => !d.status).length;
        const unread = Object.keys(unreadCounts).some(k => k.startsWith(item.id + ':')
            && (unreadCounts[k] || 0) > (readCounts[k] || 0)
            && (!currentUser || isMyReport || k === item.id + ':' + currentUser.email.toLowerCase()));
        const pref = item.preferred_contact || 'both';
        const canSeeContact = item.contact_email !== undefined;
        const contactBits = [];
        if (canSeeContact && (pref === 'email' || pref === 'both') && item.contact_email) contactBits.push(escapeHtml(item.contact_email));
        if (canSeeContact && (pref === 'phone' || pref === 'both') && item.contact_phone) contactBits.push(escapeHtml(item.contact_phone));
        const contactLine = !contactBits.length ? '' : canSeeContact
            ? `<div class="flex items-center justify-between"><span><strong>${isLost ? 'Reach me via' : 'Contact finder'}:</strong></span><span class="font-semibold text-slate-900">${contactBits.join(' &middot; ')}</span></div>`
            : `<div class="flex items-center justify-between"><span><strong>Contact:</strong></span><span class="text-slate-500">Shown after you submit a claim request</span></div>`;

        grid.innerHTML += `
            <div class="bg-white rounded-2xl overflow-hidden shadow-sm border border-slate-200 hover:shadow-lg transition flex flex-col justify-between">
                <div>
                    <div class="relative h-48 w-full bg-slate-100 overflow-hidden">
                        <img src="${item.image_url}" alt="${escapeHtml(item.title)}" class="w-full h-full object-cover">
                        <div class="absolute top-3 left-3">
                            <span class="px-3 py-1 rounded-full text-xs font-extrabold uppercase border bg-white/95 ${badgeBg}">${item.item_type}</span>
                        </div>
                        <div class="absolute top-3 right-3">
                            <span class="px-3 py-1 rounded-full text-xs font-bold border bg-white/95 ${statusBg}">${item.status}</span>
                        </div>
                    </div>
                    <div class="p-5 space-y-3">
                        <div>
                            <span class="text-xs font-bold text-slate-500">${escapeHtml(item.category)}</span>
                            <h3 class="text-lg font-extrabold text-slate-900 leading-snug mt-0.5">${escapeHtml(item.title)}</h3>
                        </div>
                        <p class="text-slate-600 text-sm leading-relaxed line-clamp-3">${escapeHtml(item.description)}</p>
                        ${disputeCount ? `<div class="bg-amber-50 border border-amber-200 text-amber-800 text-xs rounded-lg px-3 py-2 font-semibold">${disputeCount} dispute report${disputeCount > 1 ? 's' : ''} received &mdash; verify ownership before handover. <button onclick="viewDisputes(${item.id})" class="underline font-bold">Review</button></div>` : ''}
                        <div class="bg-slate-50 p-3 rounded-lg space-y-1.5 text-xs text-slate-600 border border-slate-100">
                            <div class="flex items-center justify-between">
                                <span><strong>Location:</strong></span>
                                <span class="font-semibold text-slate-900">${escapeHtml(item.location)}</span>
                            </div>
                            <div class="flex items-center justify-between">
                                <span><strong>Date:</strong></span>
                                <span class="font-semibold text-slate-900">${escapeHtml(item.date)}</span>
                            </div>
                            <div class="flex items-center justify-between">
                                <span><strong>Reporter:</strong></span>
                                <span class="font-semibold text-slate-900">${escapeHtml(item.contact_name)} (${escapeHtml(item.reporter_id)})</span>
                            </div>
                            ${contactLine}
                            ${custodyNote ? `<div class="flex items-center justify-between"><span><strong>Custody:</strong></span><span class="font-semibold text-slate-900">${custodyNote}</span></div>` : ''}
                            ${item.security_personnel ? `<div class="flex items-center justify-between pt-1 border-t border-slate-200">
                                <span class="text-emerald-700"><strong>Report To:</strong></span>
                                <span class="font-bold text-slate-900">${escapeHtml(item.security_personnel)}</span>
                            </div>` : ''}
                        </div>
                    </div>
                </div>
                <div class="px-5 pb-5 flex items-center gap-2">
                    ${item.status === 'Active' ? (
                        isMyReport
                            ? `<div class="flex-1 bg-slate-50 text-slate-500 py-2.5 rounded-lg text-xs font-bold text-center border border-slate-200">Your report &middot; ${isLost && item.found_reports_count ? `${item.found_reports_count} finder response${item.found_reports_count > 1 ? 's' : ''}` : 'awaiting a response'}</div>${isLost ? `<button onclick="markFound(${item.id})" class="bg-emerald-50 text-emerald-700 hover:bg-emerald-100 px-3 py-2.5 rounded-lg text-xs font-bold border border-emerald-200 transition" title="Item is back with me">Mark as Found</button><button onclick="closeReport(${item.id})" class="bg-slate-100 text-slate-500 hover:bg-rose-50 hover:text-rose-600 px-3 py-2.5 rounded-lg text-xs font-bold transition" title="Close this report without marking a return">Close</button>` : ''}${item.found_reports_count ? `<button onclick="viewFinders(${item.id})" class="bg-amber-50 text-amber-700 hover:bg-amber-100 px-3 py-2.5 rounded-lg text-xs font-bold border border-amber-200 transition">View</button>` : ''}`
                            : isLost
                                ? (myFoundReport
                                    ? `<button onclick="openChat(${item.id}, '${titleAttr}')" class="relative flex-1 bg-emerald-50 text-emerald-700 py-2.5 rounded-lg text-xs font-bold border border-emerald-200 hover:bg-emerald-100 transition">${unread ? '<span class="absolute -top-1 -right-1 w-2.5 h-2.5 bg-rose-500 rounded-full border border-white"></span>' : ''}Chat with Owner</button>`
                                    : `<button onclick="openFoundModal(${item.id}, '${titleAttr}')" class="flex-1 bg-emerald-600 text-white py-2.5 rounded-lg text-xs font-bold hover:bg-emerald-700 transition">I Found This Item</button>`)
                                : isRejectedClaimant
                                    ? `<div class="flex-1 bg-rose-50 text-rose-600 py-2.5 rounded-lg text-xs font-bold text-center border border-rose-200">Your claim was rejected for this item</div>`
                                    : `<button onclick="openClaimModal(${item.id}, '${titleAttr}')" class="flex-1 bg-emerald-600 text-white py-2.5 rounded-lg text-xs font-bold hover:bg-emerald-700 transition">Claim &amp; Verify Ownership</button>`
                    ) : item.status === 'Claim Requested' ? `
                        ${isMyReport ? `<button onclick="confirmReturn(${item.id})" class="flex-1 bg-emerald-600 text-white py-2.5 rounded-lg text-xs font-bold hover:bg-emerald-700 transition">Confirm Returned to Owner</button><button onclick="rejectClaim(${item.id})" class="bg-rose-50 text-rose-600 hover:bg-rose-100 px-3 py-2.5 rounded-lg text-xs font-bold transition border border-rose-200">Reject</button><button onclick="openChat(${item.id}, '${titleAttr}')" class="relative bg-slate-100 text-slate-700 hover:bg-slate-200 px-3 py-2.5 rounded-lg text-xs font-bold transition">${unread ? '<span class="absolute -top-1 -right-1 w-2.5 h-2.5 bg-rose-500 rounded-full border border-white"></span>' : ''}Chat</button>` : isMyClaim ? `<button onclick="openEditClaim(${item.id})" class="flex-1 bg-blue-50 text-blue-700 hover:bg-blue-100 py-2.5 rounded-lg text-xs font-bold border border-blue-200 transition">View / Edit My Claim</button><button onclick="openChat(${item.id}, '${titleAttr}')" class="relative bg-slate-100 text-slate-700 hover:bg-slate-200 px-3 py-2.5 rounded-lg text-xs font-bold transition">${unread ? '<span class="absolute -top-1 -right-1 w-2.5 h-2.5 bg-rose-500 rounded-full border border-white"></span>' : ''}Chat</button>` : `<div class="flex-1 bg-blue-50 text-blue-700 py-2.5 rounded-lg text-xs font-bold text-center border border-blue-200">Claim in progress</div><button onclick="openDisputeModal(${item.id}, '${titleAttr}')" class="bg-rose-50 text-rose-600 hover:bg-rose-100 px-3 py-2.5 rounded-lg text-xs font-bold transition border border-rose-200">Report Item</button>`}
                    ` : item.status === 'Closed' ? `
                        <div class="flex-1 bg-slate-100 text-slate-600 py-2.5 rounded-lg text-xs font-bold text-center border border-slate-200">Report Closed by Reporter</div>
                    ` : `
                        <div class="flex-1 bg-emerald-50 text-emerald-700 py-2.5 rounded-lg text-xs font-bold text-center border border-emerald-200">${item.resolved_via && item.resolved_via !== 'marked-found' ? escapeHtml(item.resolved_via) : 'Returned to Owner'}</div>
                    `}
                    ${isMyReport && item.status === 'Active' ? `<button onclick="openEditModal(${item.id})" class="bg-blue-50 text-blue-700 hover:bg-blue-100 px-3 py-2.5 rounded-lg text-xs font-bold border border-blue-200 transition" title="Edit Report">Edit</button>` : ''}
                    ${isMyReport ? `<button onclick="deleteItem(${item.id})" class="bg-slate-100 text-slate-500 hover:bg-rose-50 hover:text-rose-600 px-3 py-2.5 rounded-lg text-xs font-bold transition" title="Delete Report">Delete</button>` : ''}
                </div>
            </div>`;
    });
}

async function submitItem(e) {
    e.preventDefault();
    if (!requireSignIn()) return;

    const typeSel = document.getElementById('item_type').value;
    const locSel = document.getElementById('location').value;
    const catSel = document.getElementById('category').value;
    const location = locSel === 'other' ? (document.getElementById('other_location').value.trim() || 'Other Campus Location') : locSel;
    const category = catSel === 'other' ? (document.getElementById('other_category').value.trim() || 'Other') : catSel;
    const pref = document.querySelector('input[name="preferred_contact"]:checked').value;

    const formData = new FormData();
    formData.append('title', document.getElementById('title').value);
    formData.append('description', document.getElementById('description').value);
    formData.append('category', category);
    formData.append('location', location);
    formData.append('date', document.getElementById('date').value);
    formData.append('item_type', typeSel);
    formData.append('contact_name', currentUser.name);
    formData.append('contact_email', currentUser.email);
    formData.append('contact_phone', document.getElementById('contact_phone').value);
    formData.append('reporter_id', document.getElementById('reporter_id').value);
    const secSel = document.getElementById('security_personnel').value;
    formData.append('security_personnel', secSel === 'other' ? (document.getElementById('other_security').value.trim() || 'Other') : secSel);
    formData.append('preferred_contact', pref);
    if (typeSel === 'found') formData.append('custody', document.getElementById('custody').value);

    const imageFile = document.getElementById('image_file').files[0];
    if (imageFile) formData.append('image', imageFile);

    const res = await fetch('/api/items', { method: 'POST', body: formData });

    if (res.ok) {
        document.getElementById('reportForm').reset();
        document.getElementById('date').valueAsDate = new Date();
        document.getElementById('custodyWrap').classList.add('hidden');
        document.getElementById('otherLocationWrap').classList.add('hidden');
        document.getElementById('otherCategoryWrap').classList.add('hidden');
        document.getElementById('otherSecurityWrap').classList.add('hidden');
        document.getElementById('similarWrap').classList.add('hidden');
        prefillFromProfile();
        switchTab('browse');
    } else {
        let msg = 'Error submitting report. Please check all fields.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

let claimEditMode = false;
let claimEditItemId = null;

// ---- Finder response flow (lost items) ----
let foundItemId = null;

function openFoundModal(id, title) {
    if (!requireSignIn()) return;
    foundItemId = id;
    document.getElementById('foundItemTitle').innerText = title;
    if (currentUser) {
        document.getElementById('finder_name').value = currentUser.name || '';
        document.getElementById('finder_email').value = currentUser.email || '';
        if (currentUser.matric) document.getElementById('finder_id').value = currentUser.matric;
    }
    document.getElementById('foundModal').classList.remove('hidden');
}

function closeFoundModal() {
    document.getElementById('foundModal').classList.add('hidden');
    foundItemId = null;
}

async function submitFoundReport(e) {
    e.preventDefault();
    if (foundItemId === null) return;
    const res = await fetch(`/api/items/${foundItemId}/found-report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            finder_name: document.getElementById('finder_name').value,
            finder_email: document.getElementById('finder_email').value,
            finder_phone: document.getElementById('finder_phone').value,
            finder_id: document.getElementById('finder_id').value,
            location_found: document.getElementById('location_found').value,
            message: document.getElementById('finder_message').value
        })
    });
    if (res.ok) {
        const data = await res.json();
        closeFoundModal();
        document.getElementById('foundForm').reset();
        loadItems();
        alert(data.message);
    } else {
        let msg = 'Could not send your response. Please check the details.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

async function viewFinders(id) {
    if (!requireSignIn()) return;
    const item = itemsCache[id];
    if (!item || !(item.found_reports_count > 0)) return;
    const res = await fetch(`/api/items/${id}/finders?reporter_email=${encodeURIComponent(currentUser.email)}`);
    if (!res.ok) { alert('Only the reporter can view finder responses.'); return; }
    const reports = await res.json();
    document.getElementById('findersItemTitle').innerText = item.title;
    const list = document.getElementById('findersList');
    const titleAttr = escapeHtml(item.title).replace(/'/g, "\'");
    list.innerHTML = reports.map(f => `
        <div class="border border-slate-200 rounded-lg p-3 space-y-1">
            <div class="flex justify-between items-start gap-2">
                <div class="text-sm font-bold text-slate-900">${escapeHtml(f.finder_name)} <span class="text-xs font-normal text-slate-500">(${escapeHtml(f.finder_id)})</span></div>
                <span class="text-[10px] text-slate-400">${f.time}</span>
            </div>
            <div class="text-xs text-slate-500">${escapeHtml(f.finder_email)} &middot; ${escapeHtml(f.finder_phone)}</div>
            <p class="text-sm text-slate-700"><strong>Found at:</strong> ${escapeHtml(f.location_found)}</p>
            ${f.message ? `<p class="text-sm text-slate-600">${escapeHtml(f.message)}</p>` : ''}
            <div class="flex gap-2">
                <button onclick="closeFindersModal(); openChat(${id}, '${titleAttr}', '${f.finder_email}')" class="bg-emerald-600 text-white px-3 py-2 rounded-lg text-xs font-bold hover:bg-emerald-700 transition">Open Chat</button>
                <button onclick="markFound(${id}, '${f.finder_email}')" class="bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-2 rounded-lg text-xs font-bold hover:bg-emerald-100 transition">Confirm Return via This Finder</button>
            </div>
        </div>`).join('');
    document.getElementById('findersModal').classList.remove('hidden');
}

function closeFindersModal() {
    document.getElementById('findersModal').classList.add('hidden');
}

// ---- Similar-item warnings while reporting ----
let similarTimer = null;

async function checkSimilar() {
    const wrap = document.getElementById('similarWrap');
    const title = document.getElementById('title').value.trim();
    const type = document.getElementById('item_type').value;
    if (title.length < 3) { wrap.classList.add('hidden'); wrap.innerHTML = ''; return; }
    try {
        const res = await fetch(`/api/items/similar?title=${encodeURIComponent(title)}&category=${encodeURIComponent(document.getElementById('category').value)}`);
        if (!res.ok) { wrap.classList.add('hidden'); return; }
        const matches = await res.json();
        if (!matches.length) { wrap.classList.add('hidden'); wrap.innerHTML = ''; return; }
        wrap.innerHTML = `
            <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 space-y-2">
                <h4 class="text-sm font-extrabold text-amber-800">Possible matches already on the portal (${matches.length})</h4>
                <p class="text-xs text-amber-700">Check these before submitting &mdash; your ${type === 'lost' ? 'lost item may already have been found by someone' : 'found item may already be being searched for'}.</p>
                ${matches.map(m => `
                    <button type="button" onclick="switchTab('browse')" class="w-full flex items-center gap-3 bg-white border border-amber-200 rounded-lg p-2 text-left hover:bg-amber-100 transition">
                        <img src="${m.image_url}" class="w-10 h-10 rounded object-cover" alt="">
                        <div class="flex-1 min-w-0">
                            <div class="text-sm font-bold text-slate-900 truncate">${escapeHtml(m.title)}</div>
                            <div class="text-xs text-slate-500">${m.item_type} &middot; ${escapeHtml(m.location)} &middot; ${escapeHtml(m.date)} &middot; ${m.status}</div>
                        </div>
                        <span class="text-xs font-bold text-emerald-700">${Math.round(m.score * 100)}% match</span>
                    </button>`).join('')}
            </div>`;
        wrap.classList.remove('hidden');
    } catch (e) { wrap.classList.add('hidden'); }
}

function openClaimModal(id, title) {
    if (!requireSignIn()) return;
    claimEditMode = false;
    claimEditItemId = null;
    document.getElementById('claimItemId').value = id;
    document.getElementById('modalItemTitle').innerText = title;
    document.getElementById('claimSubmitBtn').innerText = 'Submit Verification Request';
    if (currentUser) {
        document.getElementById('claimant_name').value = currentUser.name || '';
    }
    updateClaimContactInfo();
    document.getElementById('claimModal').classList.remove('hidden');
}

async function openEditClaim(id) {
    if (!requireSignIn()) return;
    const item = itemsCache[id];
    if (!item) return;
    const res = await fetch(`/api/items/${id}/claim?claimant_email=${encodeURIComponent(currentUser.email)}`);
    if (!res.ok) { alert('Only the claimant who submitted this claim can view it.'); return; }
    const details = await res.json();
    claimEditMode = true;
    claimEditItemId = id;
    document.getElementById('claimItemId').value = id;
    document.getElementById('modalItemTitle').innerText = item.title;
    document.getElementById('claimant_name').value = details.claimant_name || '';
    document.getElementById('claimant_id').value = details.claimant_id || '';
    document.getElementById('claimant_phone').value = details.contact_phone || '';
    document.getElementById('proof_description').value = details.proof_description || '';
    document.getElementById('claimSubmitBtn').innerText = 'Save Changes';
    updateClaimContactInfo();
    document.getElementById('claimModal').classList.remove('hidden');
}

function updateClaimContactInfo() {
    const box = document.getElementById('claimContactInfo');
    if (!box) return;
    const id = parseInt(document.getElementById('claimItemId').value, 10);
    const item = itemsCache[id];
    if (!item) { box.innerHTML = ''; return; }
    const method = document.querySelector('input[name="contact_method"]:checked').value;
    if (method === 'email') {
        box.innerHTML = `An email will be sent to <strong>${escapeHtml(item.contact_email || 'the reporter')}</strong> containing everything you filled in above. You can edit the message before sending.`;
    } else {
        box.innerHTML = `You will chat privately in-app with <strong>${escapeHtml(item.contact_name)}</strong> about this item.`;
    }
}

function closeClaimModal() {
    document.getElementById('claimModal').classList.add('hidden');
    document.getElementById('claimForm').reset();
    claimEditMode = false;
    claimEditItemId = null;
}

async function submitClaim(e) {
    e.preventDefault();
    const id = document.getElementById('claimItemId').value;

    if (claimEditMode) {
        const payload = {
            claimant_name: document.getElementById('claimant_name').value,
            claimant_id: document.getElementById('claimant_id').value,
            contact_phone: document.getElementById('claimant_phone').value,
            claimant_email: currentUser ? currentUser.email : '',
            proof_description: document.getElementById('proof_description').value
        };
        const res = await fetch(`/api/items/${id}/claim`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            closeClaimModal();
            loadItems();
        } else {
            let msg = 'Could not update the claim.';
            try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
            alert(msg);
        }
        return;
    }

    const fd = new FormData();
    fd.append('claimant_name', document.getElementById('claimant_name').value);
    fd.append('claimant_id', document.getElementById('claimant_id').value);
    fd.append('contact_phone', document.getElementById('claimant_phone').value);
    fd.append('claimant_email', currentUser ? currentUser.email : '');
    fd.append('proof_description', document.getElementById('proof_description').value);
    const proofFile = document.getElementById('proof_image').files[0];
    if (proofFile) fd.append('proof_image', proofFile);

    const res = await fetch(`/api/items/${id}/claim`, { method: 'POST', body: fd });

    if (res.ok) {
        const data = await res.json();
        const method = document.querySelector('input[name="contact_method"]:checked').value;
        closeClaimModal();
        loadItems();
        if (method === 'email') {
            const subject = encodeURIComponent('AFIT Lost & Found: claim for "' + data.item.title + '"');
            const cName = document.getElementById('claimant_name').value.trim(), cId = document.getElementById('claimant_id').value.trim(), cPhone = document.getElementById('claimant_phone').value.trim(), cProof = document.getElementById('proof_description').value.trim();
            const body = encodeURIComponent('Hello ' + data.item.contact_name + ',\n\nI have submitted a claim for the item "' + data.item.title + '" you reported on the AFIT Lost & Found Portal.\n\nProof of ownership details: ' + cProof + '\n\nMy contact: ' + cName + ' (' + cId + ', ' + cPhone + ')\n\nPlease arrange verification and return.\n\nThank you.');
            window.location.href = 'mailto:' + data.item.contact_email + '?subject=' + subject + '&body=' + body;
        } else {
            openChat(data.item.id, data.item.title);
        }
    } else {
        let msg = 'Verification failed. Please try again.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

async function deleteItem(id) {
    if (!requireSignIn()) return;
    if (confirm('Are you sure you want to delete this security report?')) {
        const res = await fetch(`/api/items/${id}?reporter_email=${encodeURIComponent(currentUser.email)}`, { method: 'DELETE' });
        if (res.ok) {
            loadItems();
        } else {
            let msg = 'Could not delete this report.';
            try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
            alert(msg);
        }
    }
}

async function confirmReturn(id) {
    if (!requireSignIn()) return;
    const res = await fetch(`/api/items/${id}/confirm-return`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reporter_email: currentUser.email })
    });
    if (res.ok) {
        const data = await res.json();
        alert(data.message);
        loadItems();
    } else {
        let msg = 'Could not confirm return.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

/* ---- Private 1-to-1 chat (claimant <-> reporter) ---- */
let chatItemId = null;
let chatTimer = null;

let chatPeer = null;

function openChat(id, title, peerOverride) {
    if (!requireSignIn()) return;
    const item = itemsCache[id];
    let peer = peerOverride || null;
    if (item && !peer) {
        const reporter = (item.contact_email || '').toLowerCase();
        if (item.viewer_is_reporter) peer = item.active_claimant_email || null;
        else if (item.viewer_is_claimant || item.viewer_is_finder) peer = reporter;
    }
    if (item && !peer) {
        alert('This chat is private between the reporter and the person who responded.');
        return;
    }
    chatItemId = id;
    chatPeer = peer;
    document.getElementById('chatItemTitle').innerText = title;
    document.getElementById('chatModal').classList.remove('hidden');
    fetchMessages();
    clearInterval(chatTimer);
    chatTimer = setInterval(fetchMessages, 4000);
}

function closeChat() {
    document.getElementById('chatModal').classList.add('hidden');
    clearInterval(chatTimer);
    chatTimer = null;
    chatItemId = null;
    chatPeer = null;
}

async function fetchMessages() {
    if (chatItemId === null || !currentUser) return;
    const res = await fetch(`/api/items/${chatItemId}/messages?user_email=${encodeURIComponent(currentUser.email)}&peer=${encodeURIComponent(chatPeer || '')}`);
    if (!res.ok) {
        const box = document.getElementById('chatMessages');
        box.innerHTML = `<p class="text-xs text-rose-600 text-center py-6">This chat is private between the reporter and the person who responded.<br>You are signed in as <strong>${escapeHtml(currentUser.email)}</strong>.<br>Sign in with the reporter's or finder's email to join.</p>`;
        return;
    }
    const msgs = await res.json();
    const threadKey = `${chatItemId}:${(chatPeer || '').toLowerCase()}`;
    readCounts[threadKey] = msgs.length;
    saveReadCounts();
    const box = document.getElementById('chatMessages');
    box.innerHTML = msgs.length === 0
        ? '<p class="text-xs text-slate-400 text-center py-6">No messages yet. Start the conversation to arrange the return.</p>'
        : msgs.map(m => {
            const mine = m.sender_email === currentUser.email.toLowerCase();
            return `<div class="flex ${mine ? 'justify-end' : 'justify-start'}">
                <div class="${mine ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-800'} max-w-[80%] px-3 py-2 rounded-2xl text-sm">
                    <div class="text-[10px] font-bold opacity-70 mb-0.5">${escapeHtml(m.sender_name)} &middot; ${m.time}</div>
                    ${escapeHtml(m.text)}
                </div>
            </div>`;
        }).join('');
    box.scrollTop = box.scrollHeight;
}

async function sendChatMessage(e) {
    e.preventDefault();
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text || chatItemId === null || !currentUser) return;
    const res = await fetch(`/api/items/${chatItemId}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            sender_name: currentUser.name,
            sender_email: currentUser.email,
            sender_role: 'claimant',
            text: text,
            peer_email: chatPeer || ''
        })
    });
    if (!res.ok) {
        let msg = 'Message could not be sent.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
        return;
    }
    input.value = '';
    fetchMessages();
}

function openDisputeModal(id, title) {
    document.getElementById('disputeItemId').value = id;
    document.getElementById('disputeItemTitle').innerText = title;
    if (currentUser) {
        document.getElementById('dispute_name').value = currentUser.name || '';
        document.getElementById('dispute_email').value = currentUser.email || '';
    }
    document.getElementById('disputeModal').classList.remove('hidden');
}

function closeDisputeModal() {
    document.getElementById('disputeModal').classList.add('hidden');
    document.getElementById('disputeForm').reset();
}

async function submitDispute(e) {
    e.preventDefault();
    const id = document.getElementById('disputeItemId').value;
    const payload = {
        name: document.getElementById('dispute_name').value,
        email: document.getElementById('dispute_email').value,
        message: document.getElementById('dispute_message').value
    };
    const res = await fetch(`/api/items/${id}/dispute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    if (res.ok) {
        const data = await res.json();
        closeDisputeModal();
        loadItems();
        alert(data.message);
    } else {
        let msg = 'Could not submit the report.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

function viewDisputes(id) {
    const item = itemsCache[id];
    if (!item || !(item.disputes || []).length) return;
    document.getElementById('disputeViewItemTitle').innerText = item.title;
    const isReporter = currentUser && currentUser.email.toLowerCase() === (item.contact_email || '').toLowerCase();
    const list = document.getElementById('disputesList');
    list.innerHTML = item.disputes.map((d, idx) => {
        const statusBadge = d.status === 'upheld'
            ? '<span class="text-[10px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-full px-2 py-0.5">UPHELD - claim rejected</span>'
            : d.status === 'dismissed'
                ? '<span class="text-[10px] font-bold text-slate-500 bg-slate-100 border border-slate-200 rounded-full px-2 py-0.5">DISMISSED</span>'
                : '';
        const actions = (!d.status && isReporter && item.status === 'Claim Requested')
            ? `<div class="flex gap-2 mt-2">
                    <a href="mailto:${encodeURIComponent(d.email)}?subject=${encodeURIComponent('AFIT Lost & Found: dispute review for "' + item.title + '"')}" class="bg-slate-100 text-slate-700 hover:bg-slate-200 px-3 py-2 rounded-lg text-xs font-bold transition">Email ${escapeHtml(d.email)}</a>
                    <button onclick="resolveDispute(${id}, ${idx}, 'uphold')" class="bg-emerald-600 text-white px-3 py-2 rounded-lg text-xs font-bold hover:bg-emerald-700 transition">Uphold: reject claim</button>
                    <button onclick="resolveDispute(${id}, ${idx}, 'dismiss')" class="bg-slate-100 text-slate-600 hover:bg-slate-200 px-3 py-2 rounded-lg text-xs font-bold transition">Dismiss</button>
                </div>`
            : (!isReporter ? '<p class="text-[10px] text-slate-400 mt-1">Only the reporter can resolve disputes.</p>' : '');
        return `<div class="border border-slate-200 rounded-lg p-3 space-y-1">
            <div class="flex justify-between items-start gap-2">
                <div class="text-sm font-bold text-slate-900">${escapeHtml(d.name)}</div>
                ${statusBadge}
            </div>
            <div class="text-xs text-slate-500">${escapeHtml(d.email)} &middot; ${d.time}</div>
            <p class="text-sm text-slate-700">${escapeHtml(d.message)}</p>
            ${actions}
        </div>`;
    }).join('');
    document.getElementById('disputeViewModal').classList.remove('hidden');
}

function closeDisputeViewModal() {
    document.getElementById('disputeViewModal').classList.add('hidden');
}

let editItemId = null;

function openEditModal(id) {
    if (!requireSignIn()) return;
    const item = itemsCache[id];
    if (!item || !item.viewer_is_reporter) return;
    editItemId = id;
    document.getElementById('editItemTitle').innerText = item.title;
    document.getElementById('edit_title').value = item.title || '';
    document.getElementById('edit_description').value = item.description || '';
    document.getElementById('edit_category').value = item.category || '';
    document.getElementById('edit_location').value = item.location || '';
    document.getElementById('edit_date').value = item.date || '';
    document.getElementById('edit_security').value = item.security_personnel || '';
    document.getElementById('edit_contact_name').value = item.contact_name || '';
    document.getElementById('edit_contact_phone').value = item.contact_phone || '';
    document.getElementById('edit_reporter_id').value = item.reporter_id || '';
    document.getElementById('edit_email_label').innerText = item.contact_email || currentUser.email;
    document.getElementById('editCustodyWrap').classList.toggle('hidden', item.item_type !== 'found');
    if (item.item_type === 'found') document.getElementById('edit_custody').value = item.custody || 'security';
    const pref = item.preferred_contact || 'both';
    document.querySelector(`input[name="edit_pref"][value="${pref}"]`).checked = true;
    document.getElementById('edit_image').value = '';
    document.getElementById('editModal').classList.remove('hidden');
}

function closeEditModal() {
    document.getElementById('editModal').classList.add('hidden');
    editItemId = null;
}

async function submitEdit(e) {
    e.preventDefault();
    if (editItemId === null) return;
    const fd = new FormData();
    fd.append('reporter_email', currentUser.email);
    fd.append('title', document.getElementById('edit_title').value);
    fd.append('description', document.getElementById('edit_description').value);
    fd.append('category', document.getElementById('edit_category').value);
    fd.append('location', document.getElementById('edit_location').value);
    fd.append('date', document.getElementById('edit_date').value);
    fd.append('preferred_contact', document.querySelector('input[name="edit_pref"]:checked').value);
    fd.append('security_personnel', document.getElementById('edit_security').value);
    fd.append('contact_name', document.getElementById('edit_contact_name').value);
    fd.append('contact_phone', document.getElementById('edit_contact_phone').value);
    fd.append('reporter_id', document.getElementById('edit_reporter_id').value);
    if (!document.getElementById('editCustodyWrap').classList.contains('hidden')) {
        fd.append('custody', document.getElementById('edit_custody').value);
    }
    const imgFile = document.getElementById('edit_image').files[0];
    if (imgFile) fd.append('image', imgFile);
    const res = await fetch(`/api/items/${editItemId}`, { method: 'PUT', body: fd });
    if (res.ok) {
        const data = await res.json();
        closeEditModal();
        loadItems();
        alert(data.message);
    } else {
        let msg = 'Could not update the report.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

async function closeReport(id) {
    if (!requireSignIn()) return;
    if (!confirm('Close this report? It will no longer appear as active on the portal.')) return;
    const res = await fetch(`/api/items/${id}/close-report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reporter_email: currentUser.email })
    });
    if (res.ok) {
        const data = await res.json();
        loadItems();
        alert(data.message);
    } else {
        let msg = 'Could not close the report.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

async function markFound(id, finderEmail) {
    if (!requireSignIn()) return;
    if (!confirm(finderEmail ? 'Confirm this item was returned by this finder?' : 'Mark this item as found and returned to you?')) return;
    const res = await fetch(`/api/items/${id}/mark-found`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reporter_email: currentUser.email, finder_email: finderEmail || '' })
    });
    if (res.ok) {
        const data = await res.json();
        loadItems();
        alert(data.message);
    } else {
        let msg = 'Could not update the item.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

async function resolveDispute(id, index, action) {
    if (!requireSignIn()) return;
    const verb = action === 'uphold' ? 'reject the current claim and mark this dispute upheld' : 'dismiss this dispute (the current claim stands)';
    if (!confirm(`Are you sure you want to ${verb}?`)) return;
    const res = await fetch(`/api/items/${id}/disputes/${index}/resolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reporter_email: currentUser.email, action: action })
    });
    if (res.ok) {
        const data = await res.json();
        closeDisputeViewModal();
        loadItems();
        alert(data.message);
    } else {
        let msg = 'Could not resolve the dispute.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

async function rejectClaim(id) {
    if (!requireSignIn()) return;
    if (!confirm('Reject this claim request? The item will return to Active.')) return;
    const res = await fetch(`/api/items/${id}/reject-claim`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reporter_email: currentUser.email })
    });
    if (res.ok) {
        const data = await res.json();
        alert(data.message);
        loadItems();
    } else {
        let msg = 'Could not reject the claim.';
        try { const err = await res.json(); if (err.detail) msg = err.detail; } catch (err) {}
        alert(msg);
    }
}

function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

// Initial load
renderAuthArea();
prefillFromProfile();
loadItems();

// Live duplicate warning while typing a report title
document.getElementById('title').addEventListener('input', () => {
    clearTimeout(similarTimer);
    similarTimer = setTimeout(checkSimilar, 500);
});

// PWA: register service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js').catch(() => {});
    });
}

// Light polling: refresh unread chat badges while on the browse tab
setInterval(() => {
    const browse = document.getElementById('section-browse');
    if (browse && !browse.classList.contains('hidden') && !chatTimer) {
        loadItems();
    }
}, 15000);
