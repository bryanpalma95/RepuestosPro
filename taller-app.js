(function () {
    'use strict';

    let repo;
    const ONBOARDING_STORAGE_KEY = 'repuestospro:taller:onboarding-hidden:v1';
    const APPEARANCE_STORAGE_KEY = 'repuestospro:appearance:v1';
    const state = {
        section: 'clients', query: '', catalog: {}, detail: null, pendingVehicle: false,
        pricingTimer: null, catalogSearchTimer: null, partPicker: null, catalogResults: new Map(), selectedCatalogPart: null,
        summary: null, pendingLineAfterService: null
    };
    const els = {
        clientCount: document.getElementById('clientCount'), vehicleCount: document.getElementById('vehicleCount'),
        orderCount: document.getElementById('orderCount'), serviceCount: document.getElementById('serviceCount'),
        catalogStatus: document.getElementById('catalogStatus'), recordList: document.getElementById('recordList'),
        recordSearch: document.getElementById('recordSearch'), resultCount: document.getElementById('resultCount'),
        workspaceTitle: document.getElementById('workspaceTitle'), workspaceEyebrow: document.getElementById('workspaceEyebrow'),
        addRecordButton: document.getElementById('addRecordButton'), listView: document.getElementById('listView'),
        detailView: document.getElementById('detailView'), detailContent: document.getElementById('detailContent'),
        clientsTab: document.getElementById('clientsTab'), vehiclesTab: document.getElementById('vehiclesTab'),
        ordersTab: document.getElementById('ordersTab'), servicesTab: document.getElementById('servicesTab'),
        clientDialog: document.getElementById('clientDialog'), vehicleDialog: document.getElementById('vehicleDialog'),
        serviceDialog: document.getElementById('serviceDialog'), orderDialog: document.getElementById('orderDialog'),
        lineDialog: document.getElementById('lineDialog'), partPickerDialog: document.getElementById('partPickerDialog'),
        partLineDialog: document.getElementById('partLineDialog'), manualPartDialog: document.getElementById('manualPartDialog'),
        pendingPartsDialog: document.getElementById('pendingPartsDialog'), clientForm: document.getElementById('clientForm'),
        vehicleForm: document.getElementById('vehicleForm'), serviceForm: document.getElementById('serviceForm'),
        orderForm: document.getElementById('orderForm'), lineForm: document.getElementById('lineForm'),
        partLineForm: document.getElementById('partLineForm'), manualPartForm: document.getElementById('manualPartForm'),
        clientFormError: document.getElementById('clientFormError'), vehicleFormError: document.getElementById('vehicleFormError'),
        serviceFormError: document.getElementById('serviceFormError'), orderFormError: document.getElementById('orderFormError'),
        lineFormError: document.getElementById('lineFormError'), partLineFormError: document.getElementById('partLineFormError'),
        manualPartFormError: document.getElementById('manualPartFormError'),
        catalogContext: document.getElementById('catalogContext'), catalogPartSearch: document.getElementById('catalogPartSearch'),
        catalogResultMeta: document.getElementById('catalogResultMeta'), catalogResults: document.getElementById('catalogResults'),
        selectedPartSummary: document.getElementById('selectedPartSummary'), plateSearchForm: document.getElementById('plateSearchForm'),
        plateSearch: document.getElementById('plateSearch'), plateSearchMessage: document.getElementById('plateSearchMessage'),
        onboardingPanel: document.getElementById('onboardingPanel'), onboardingSteps: document.getElementById('onboardingSteps'),
        onboardingProgressText: document.getElementById('onboardingProgressText'), onboardingProgressBar: document.getElementById('onboardingProgressBar'),
        servicePickerEmpty: document.getElementById('servicePickerEmpty'), toast: document.getElementById('toast'),
        pendingPartsMeta: document.getElementById('pendingPartsMeta'), pendingPartsList: document.getElementById('pendingPartsList'),
        enrichmentFileInput: document.getElementById('enrichmentFileInput'), manualPartVehicle: document.getElementById('manualPartVehicle'),
        paletteSelect: document.getElementById('paletteSelect'), paletteButton: document.getElementById('paletteButton'), palettePopover: document.getElementById('palettePopover'), paletteRange: document.getElementById('paletteRange'), themeToggle: document.getElementById('themeToggle'),
        clientSidebarCount: document.getElementById('clientSidebarCount'), vehicleSidebarCount: document.getElementById('vehicleSidebarCount'),
        orderSidebarCount: document.getElementById('orderSidebarCount'), serviceSidebarCount: document.getElementById('serviceSidebarCount'),
        dashboardClientCount: document.getElementById('dashboardClientCount'), dashboardVehicleCount: document.getElementById('dashboardVehicleCount'), dashboardOrderCount: document.getElementById('dashboardOrderCount'),
        compactPlateSearchForm: document.getElementById('compactPlateSearchForm'), compactPlateSearch: document.getElementById('compactPlateSearch'), compactPlateSearchMessage: document.getElementById('compactPlateSearchMessage')
    };
    const tabs = { clients: els.clientsTab, vehicles: els.vehiclesTab, orders: els.ordersTab, services: els.servicesTab };

    function escapeHtml(value) {
        return String(value == null ? '' : value).replace(/[&<>'"]/g, function (char) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char];
        });
    }
    function valueOrDash(value) { return value === '' || value == null ? '<span class="muted-value">Sin registrar</span>' : escapeHtml(value); }
    function formatDate(value) {
        if (!value) return 'Sin registrar';
        const date = /^\d{4}-\d{2}-\d{2}$/.test(String(value)) ? new Date(String(value) + 'T12:00:00') : new Date(value);
        return new Intl.DateTimeFormat('es-CL', { dateStyle: 'medium' }).format(date);
    }
    function formatKm(value) { return value == null || value === '' ? '' : new Intl.NumberFormat('es-CL').format(value) + ' km'; }
    function formatMoney(value) { return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(Number(value) || 0); }
    function todayValue() { const now = new Date(); return now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0'); }
    function clientName(client) { return client ? [client.nombre, client.apellido].filter(Boolean).join(' ') : 'Cliente no disponible'; }
    function vehicleName(vehicle) { return vehicle ? [vehicle.marca, vehicle.modelo, vehicle.anio].filter(Boolean).join(' ') : 'Vehículo no disponible'; }
    function showToast(message) { els.toast.textContent = message; els.toast.classList.add('visible'); clearTimeout(showToast.timer); showToast.timer = setTimeout(function () { els.toast.classList.remove('visible'); }, 2800); }
    function readAppearance() {
        try { return Object.assign({ palette: 'navy', theme: 'light' }, JSON.parse(localStorage.getItem(APPEARANCE_STORAGE_KEY) || '{}')); }
        catch (error) { return { palette: 'navy', theme: 'light' }; }
    }
    function applyAppearance(appearance) {
        const allowedPalettes = ['navy', 'copper', 'sage', 'wine', 'electric', 'teal', 'amber', 'violet'];
        const allowedThemes = ['light', 'dark'];
        const palette = allowedPalettes.includes(appearance.palette) ? appearance.palette : 'navy';
        const theme = allowedThemes.includes(appearance.theme) ? appearance.theme : 'light';
        document.documentElement.dataset.palette = palette; document.documentElement.dataset.theme = theme;
        document.documentElement.dataset.resolvedTheme = theme;
        els.paletteSelect.value = palette;
        els.paletteRange.value = String(allowedPalettes.indexOf(palette));
        els.themeToggle.textContent = theme === 'dark' ? '☾' : '☀';
        const nextThemeLabel = theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro';
        els.themeToggle.setAttribute('aria-label', nextThemeLabel); els.themeToggle.title = nextThemeLabel;
        try { localStorage.setItem(APPEARANCE_STORAGE_KEY, JSON.stringify({ palette: palette, theme: theme })); } catch (error) { /* La apariencia actual sigue aplicada. */ }
    }
    function cycleTheme() {
        const appearance = readAppearance();
        appearance.theme = appearance.theme === 'dark' ? 'light' : 'dark';
        applyAppearance(appearance);
    }
    function showError(target, error) { target.textContent = error && error.message ? error.message : String(error); }
    function setOptions(datalist, values) { datalist.replaceChildren(); values.forEach(function (value) { const option = document.createElement('option'); option.value = value; datalist.appendChild(option); }); }
    function findCatalogKey(object, input) { const wanted = String(input || '').trim().toLocaleLowerCase('es'); return Object.keys(object || {}).find(function (key) { return key.toLocaleLowerCase('es') === wanted; }); }
    function statusOptions(current) { return TallerData.WORK_ORDER_STATUSES.map(function (status) { return '<option value="' + escapeHtml(status) + '"' + (status === current ? ' selected' : '') + '>' + escapeHtml(status) + '</option>'; }).join(''); }
    function statusBadge(status) { return '<span class="status-badge" data-status="' + escapeHtml(status) + '">' + escapeHtml(status) + '</span>'; }

    async function loadCatalogNavigation() {
        try {
            const response = await fetch('db-nav.json');
            if (!response.ok) throw new Error('Respuesta no válida');
            state.catalog = await response.json();
            const brands = Object.keys(state.catalog).sort(function (a, b) { return a.localeCompare(b, 'es'); });
            setOptions(document.getElementById('brandOptions'), brands);
            els.catalogStatus.textContent = brands.length + ' marcas disponibles';
        } catch (error) {
            state.catalog = {};
            els.catalogStatus.textContent = 'Modo manual disponible';
            document.getElementById('catalogHint').textContent = 'No se pudieron cargar las sugerencias del catálogo. Puedes ingresar marca, modelo y año manualmente.';
        }
    }
    function updateModelSuggestions() {
        const brandKey = findCatalogKey(state.catalog, els.vehicleForm.elements.marca.value);
        const models = brandKey ? Object.keys(state.catalog[brandKey]).sort(function (a, b) { return a.localeCompare(b, 'es'); }) : [];
        setOptions(document.getElementById('modelOptions'), models); updateYearSuggestions();
    }
    function updateYearSuggestions() {
        const brandKey = findCatalogKey(state.catalog, els.vehicleForm.elements.marca.value);
        const modelKey = brandKey ? findCatalogKey(state.catalog[brandKey], els.vehicleForm.elements.modelo.value) : null;
        setOptions(document.getElementById('yearOptions'), modelKey ? state.catalog[brandKey][modelKey].map(String) : []);
    }
    function onboardingIsDismissed() {
        try { return localStorage.getItem(ONBOARDING_STORAGE_KEY) === '1'; } catch (error) { return false; }
    }
    function setOnboardingDismissed(dismissed) {
        try { if (dismissed) localStorage.setItem(ONBOARDING_STORAGE_KEY, '1'); else localStorage.removeItem(ONBOARDING_STORAGE_KEY); } catch (error) { /* La guía sigue funcionando sin persistencia. */ }
    }
    function renderOnboarding(summary) {
        state.summary = summary;
        const steps = [
            { title: 'Crea un cliente', copy: 'Guarda sus datos de contacto. Los vehículos y las órdenes necesitan un cliente asociado.', count: summary.clients, action: 'new-client', button: 'Crear cliente' },
            { title: 'Registra un vehículo', copy: 'Asocia patente, marca, modelo y año al cliente. Esto habilita la compatibilidad de repuestos.', count: summary.vehicles, action: 'new-vehicle', button: 'Registrar vehículo' },
            { title: 'Define tus servicios', copy: 'Crea trabajos reutilizables con precio base. Sin este paso, el selector de servicios estará vacío.', count: summary.activeServices, action: 'new-service', button: 'Crear servicio' },
            { title: 'Abre una orden', copy: 'Registra el ingreso y arma el presupuesto con servicios, mano de obra y repuestos.', count: summary.workOrders, action: 'new-order', button: 'Crear orden' }
        ];
        const completed = steps.filter(function (step) { return step.count > 0; }).length;
        els.onboardingProgressText.textContent = completed === steps.length ? 'Configuración esencial completada' : completed + ' de ' + steps.length + ' pasos listos';
        els.onboardingProgressBar.style.width = String((completed / steps.length) * 100) + '%';
        els.onboardingSteps.innerHTML = steps.map(function (step, index) {
            const complete = step.count > 0;
            return '<article class="onboarding-step" data-complete="' + complete + '">' +
                '<span class="onboarding-step-number">' + (complete ? '✓' : index + 1) + '</span>' +
                '<h3>' + step.title + '</h3><p>' + step.copy + '</p>' +
                '<span class="step-status">' + (complete ? step.count + ' registro' + (step.count === 1 ? ' listo' : 's listos') : 'Pendiente') + '</span>' +
                '<button type="button" class="button ' + (complete ? 'secondary' : 'primary') + '" data-action="' + step.action + '">' + (complete ? 'Agregar otro' : step.button) + '</button></article>';
        }).join('');
        els.onboardingPanel.hidden = onboardingIsDismissed();
    }
    function showOnboarding() {
        setOnboardingDismissed(false); els.onboardingPanel.hidden = false;
        els.onboardingPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    async function refreshSummary() {
        const summary = await repo.getSummary();
        els.clientCount.textContent = summary.clients; els.vehicleCount.textContent = summary.vehicles;
        els.orderCount.textContent = summary.workOrders; els.serviceCount.textContent = summary.activeServices;
        els.clientSidebarCount.textContent = summary.clients; els.vehicleSidebarCount.textContent = summary.vehicles;
        els.orderSidebarCount.textContent = summary.workOrders; els.serviceSidebarCount.textContent = summary.activeServices;
        els.dashboardClientCount.textContent = summary.clients; els.dashboardVehicleCount.textContent = summary.vehicles; els.dashboardOrderCount.textContent = summary.workOrders;
        renderOnboarding(summary); return summary;
    }

    const sectionCopy = {
        clients: { title: 'Clientes', eyebrow: 'DIRECTORIO', add: 'Nuevo cliente', placeholder: 'Buscar por nombre, RUT, teléfono o email…' },
        vehicles: { title: 'Vehículos', eyebrow: 'PARQUE AUTOMOTRIZ', add: 'Nuevo vehículo', placeholder: 'Buscar por patente, VIN, marca, modelo o cliente…' },
        orders: { title: 'Órdenes de trabajo', eyebrow: 'OPERACIÓN DEL TALLER', add: 'Nueva orden', placeholder: 'Buscar por OT, patente, cliente, estado o problema…' },
        services: { title: 'Servicios', eyebrow: 'CATÁLOGO DEL TALLER', add: 'Nuevo servicio', placeholder: 'Buscar por nombre o descripción…' }
    };
    function emptyState(kind, hasQuery) {
        const labels = {
            clients: ['Aún no hay clientes', 'Crea la primera ficha para comenzar a organizar el taller.', 'Crear cliente', 'new-client'],
            vehicles: ['Aún no hay vehículos', 'Registra un vehículo y asócialo con uno de tus clientes.', 'Registrar vehículo', 'new-vehicle'],
            orders: ['Aún no hay órdenes', 'Crea una orden para comenzar a registrar el trabajo del taller.', 'Crear orden', 'new-order'],
            services: ['Aún no hay servicios', 'Define servicios reutilizables para preparar órdenes con rapidez.', 'Crear servicio', 'new-service']
        };
        const item = labels[kind];
        const title = hasQuery ? 'No encontramos coincidencias' : item[0];
        const copy = hasQuery ? 'Prueba con otra búsqueda o limpia el campo para ver todos los registros.' : item[1];
        return '<div class="empty-state"><strong>' + title + '</strong><p>' + copy + '</p>' + (hasQuery ? '' : '<button type="button" class="button primary" data-action="' + item[3] + '">' + item[2] + '</button>') + '</div>';
    }

    async function renderList() {
        const copy = sectionCopy[state.section];
        let records = [], clients = [], vehicles = [], orders = [];
        if (state.section === 'clients') { records = await repo.listClients(state.query); vehicles = await repo.listVehicles(''); orders = await repo.listWorkOrders(''); }
        if (state.section === 'vehicles') { records = await repo.listVehicles(state.query); clients = await repo.listClients(''); }
        if (state.section === 'orders') { records = await repo.listWorkOrders(state.query); clients = await repo.listClients(''); vehicles = await repo.listVehicles(''); }
        if (state.section === 'services') records = await repo.listServices(state.query, true);
        const clientsById = new Map(clients.map(function (client) { return [client.id, client]; }));
        const vehiclesById = new Map(vehicles.map(function (vehicle) { return [vehicle.id, vehicle]; }));
        const vehicleByClient = new Map(); vehicles.forEach(function (vehicle) { if (!vehicleByClient.has(vehicle.clienteId)) vehicleByClient.set(vehicle.clienteId, vehicle); });
        const orderByClient = new Map(); orders.forEach(function (order) { if (!orderByClient.has(order.clienteId) && !['Entregada', 'Cancelada'].includes(order.estado)) orderByClient.set(order.clienteId, order); });
        els.workspaceTitle.textContent = copy.title; els.workspaceEyebrow.textContent = copy.eyebrow;
        els.addRecordButton.textContent = copy.add; els.recordSearch.placeholder = copy.placeholder;
        els.resultCount.textContent = records.length + ' registro' + (records.length === 1 ? '' : 's');
        if (!records.length) { els.recordList.innerHTML = emptyState(state.section, Boolean(state.query)); return; }
        els.recordList.innerHTML = records.map(function (record) {
            if (state.section === 'clients') {
                const contact = record.whatsapp || record.telefono || record.email || 'Sin contacto registrado';
                const vehicle = vehicleByClient.get(record.id), order = orderByClient.get(record.id), initials = ((record.nombre || '').charAt(0) + (record.apellido || '').charAt(0)).toUpperCase() || 'CL';
                return '<button type="button" class="record-card client-record" data-kind="client" data-id="' + escapeHtml(record.id) + '"><span class="client-avatar">' + escapeHtml(initials) + '</span><span class="client-person"><strong>' + escapeHtml(clientName(record)) + '</strong><small>' + valueOrDash(record.rut) + ' · ' + escapeHtml(contact) + '</small></span><span class="client-vehicle"><strong>' + (vehicle ? escapeHtml(vehicle.marca + ' ' + vehicle.modelo) : 'Sin vehículo') + '</strong><small>' + (vehicle ? escapeHtml([vehicle.anio, vehicle.patente].filter(Boolean).join(' · ')) : 'Registra un vehículo') + '</small></span><span class="client-status ' + (order ? 'active' : '') + '">' + (order ? escapeHtml(order.estado || 'Orden activa') : 'Sin orden') + '</span></button>';
            }
            if (state.section === 'vehicles') {
                const owner = clientsById.get(record.clienteId);
                return '<button type="button" class="record-card" data-kind="vehicle" data-id="' + escapeHtml(record.id) + '"><span class="record-id">Patente ' + escapeHtml(record.patente) + '</span><h3>' + escapeHtml(vehicleName(record)) + '</h3><p>' + escapeHtml(clientName(owner)) + '</p><p>' + (record.kilometraje == null ? 'Kilometraje sin registrar' : escapeHtml(formatKm(record.kilometraje))) + '</p></button>';
            }
            if (state.section === 'orders') {
                const vehicle = vehiclesById.get(record.vehiculoId), client = clientsById.get(record.clienteId);
                return '<button type="button" class="record-card" data-kind="order" data-id="' + escapeHtml(record.id) + '"><span class="record-id">' + escapeHtml(record.identificador) + ' · ' + escapeHtml(formatDate(record.fecha)) + '</span><h3>' + escapeHtml(vehicle ? vehicle.patente + ' · ' + vehicleName(vehicle) : 'Vehículo no disponible') + '</h3><p>' + escapeHtml(clientName(client)) + '</p><p>' + escapeHtml(record.problemaReportado || 'Sin descripción') + '</p>' + statusBadge(record.estado) + '<p class="money">' + escapeHtml(formatMoney(record.totales && record.totales.total)) + '</p></button>';
            }
            return '<button type="button" class="record-card" data-kind="service" data-id="' + escapeHtml(record.id) + '"><span class="record-id">' + (record.activo ? 'Servicio activo' : 'Servicio inactivo') + '</span><h3>' + escapeHtml(record.nombre) + '</h3><p>' + escapeHtml(record.descripcion || 'Sin descripción') + '</p><p class="money">Desde ' + escapeHtml(formatMoney(record.precioBase)) + (record.duracionEstimada ? ' · ' + escapeHtml(record.duracionEstimada) + ' min' : '') + '</p></button>';
        }).join('');
    }

    function activateSectionTabs(section) { Object.keys(tabs).forEach(function (key) { tabs[key].setAttribute('aria-selected', String(key === section)); }); }
    async function setSection(section) {
        state.section = section; state.query = ''; state.detail = null; els.recordSearch.value = '';
        els.listView.hidden = false; els.detailView.hidden = true; activateSectionTabs(section); await renderList();
    }
    function detailField(label, value, wide) { return '<div class="detail-field' + (wide ? ' wide' : '') + '"><span>' + escapeHtml(label) + '</span><strong>' + valueOrDash(value) + '</strong></div>'; }

    async function showClientDetail(id) {
        const client = await repo.getClient(id); if (!client) { showToast('Cliente no encontrado.'); return setSection('clients'); }
        const vehicles = await repo.listVehicles('', id);
        state.section = 'clients'; activateSectionTabs('clients'); state.detail = { kind: 'client', id: id };
        els.listView.hidden = true; els.detailView.hidden = false;
        els.detailContent.innerHTML = '<article class="detail-hero"><div><span class="eyebrow">CLIENTE · ' + escapeHtml(client.rut) + '</span><h2>' + escapeHtml(clientName(client)) + '</h2><p>Cliente desde ' + escapeHtml(formatDate(client.createdAt)) + '</p></div><div class="detail-actions"><button type="button" class="button secondary" data-action="edit-client" data-id="' + escapeHtml(id) + '">Editar</button><button type="button" class="danger-button" data-action="delete-client" data-id="' + escapeHtml(id) + '">Eliminar</button></div></article>' +
            '<div class="detail-grid">' + detailField('ID', client.id) + detailField('RUT', client.rut) + detailField('Teléfono', client.telefono) + detailField('WhatsApp', client.whatsapp) + detailField('Email', client.email) + detailField('Dirección', client.direccion) + detailField('Notas', client.notas, true) + '</div>' +
            '<section class="related-section"><div class="related-heading"><h3>Vehículos asociados (' + vehicles.length + ')</h3><button type="button" class="button primary" data-action="new-vehicle" data-client-id="' + escapeHtml(id) + '">+ Agregar vehículo</button></div><div class="record-list">' + (vehicles.length ? vehicles.map(function (vehicle) { return '<button type="button" class="record-card" data-kind="vehicle" data-id="' + escapeHtml(vehicle.id) + '"><span class="record-id">' + escapeHtml(vehicle.patente) + '</span><h3>' + escapeHtml(vehicleName(vehicle)) + '</h3><p>' + (vehicle.kilometraje == null ? 'Kilometraje sin registrar' : escapeHtml(formatKm(vehicle.kilometraje))) + '</p></button>'; }).join('') : '<div class="empty-state"><strong>Sin vehículos asociados</strong><p>Agrega el primer vehículo de este cliente.</p></div>') + '</div></section>';
        els.detailView.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    function renderOrderHistory(orders) {
        if (!orders.length) return '<div class="empty-state"><strong>Sin órdenes previas</strong><p>La primera orden de este vehículo aparecerá aquí.</p></div>';
        return '<div class="history-list">' + orders.map(function (order) { return '<div class="history-row"><span class="history-date">' + escapeHtml(formatDate(order.fecha)) + '</span>' + statusBadge(order.estado) + '<span class="history-description">' + escapeHtml(order.problemaReportado || 'Sin descripción') + '</span><strong class="history-total money">' + escapeHtml(formatMoney(order.totales && order.totales.total)) + '</strong><button type="button" class="history-open" data-action="open-order" data-id="' + escapeHtml(order.id) + '">Abrir →</button></div>'; }).join('') + '</div>';
    }
    async function showVehicleDetail(id) {
        const vehicle = await repo.getVehicle(id); if (!vehicle) { showToast('Vehículo no encontrado.'); return setSection('vehicles'); }
        const client = await repo.getClient(vehicle.clienteId), orders = await repo.listWorkOrders('', id);
        state.section = 'vehicles'; activateSectionTabs('vehicles'); state.detail = { kind: 'vehicle', id: id };
        els.listView.hidden = true; els.detailView.hidden = false;
        els.detailContent.innerHTML = '<article class="detail-hero"><div><span class="eyebrow">PATENTE · ' + escapeHtml(vehicle.patente) + '</span><h2>' + escapeHtml(vehicleName(vehicle)) + '</h2><p>Cliente: <button type="button" class="text-action" data-action="open-client" data-id="' + escapeHtml(vehicle.clienteId) + '">' + escapeHtml(clientName(client)) + '</button></p></div><div class="detail-actions"><button type="button" class="button primary" data-action="new-order" data-vehicle-id="' + escapeHtml(id) + '">+ Nueva orden</button><button type="button" class="button secondary" data-action="edit-vehicle" data-id="' + escapeHtml(id) + '">Editar</button><button type="button" class="danger-button" data-action="delete-vehicle" data-id="' + escapeHtml(id) + '">Eliminar</button></div></article>' +
            '<div class="detail-grid">' + detailField('Patente', vehicle.patente) + detailField('VIN', vehicle.vin) + detailField('Cliente', clientName(client)) + detailField('Marca', vehicle.marca) + detailField('Modelo', vehicle.modelo) + detailField('Año', vehicle.anio) + detailField('Código o versión del motor', vehicle.motor) + detailField('Cilindrada', vehicle.cilindrada) + detailField('Combustible', vehicle.combustible) + detailField('Transmisión', vehicle.transmision) + detailField('Kilometraje', formatKm(vehicle.kilometraje)) + detailField('Color', vehicle.color) + detailField('Notas', vehicle.notas, true) + '</div>' +
            '<section class="related-section"><div class="related-heading"><h3>Historial del vehículo (' + orders.length + ')</h3><button type="button" class="button primary" data-action="new-order" data-vehicle-id="' + escapeHtml(id) + '">+ Crear orden</button></div>' + renderOrderHistory(orders) + '</section>';
        els.detailView.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    async function showServiceDetail(id) {
        const service = await repo.getService(id); if (!service) { showToast('Servicio no encontrado.'); return setSection('services'); }
        state.section = 'services'; activateSectionTabs('services'); state.detail = { kind: 'service', id: id };
        els.listView.hidden = true; els.detailView.hidden = false;
        els.detailContent.innerHTML = '<article class="detail-hero"><div><span class="eyebrow">' + (service.activo ? 'SERVICIO ACTIVO' : 'SERVICIO INACTIVO') + '</span><h2>' + escapeHtml(service.nombre) + '</h2><p>Actualizado ' + escapeHtml(formatDate(service.updatedAt)) + '</p></div><div class="detail-actions"><button type="button" class="button secondary" data-action="edit-service" data-id="' + escapeHtml(id) + '">Editar</button><button type="button" class="danger-button" data-action="delete-service" data-id="' + escapeHtml(id) + '">Eliminar</button></div></article><div class="detail-grid">' + detailField('Precio base', formatMoney(service.precioBase)) + detailField('Duración estimada', service.duracionEstimada == null ? '' : service.duracionEstimada + ' minutos') + detailField('Estado', service.activo ? 'Activo' : 'Inactivo') + detailField('Descripción', service.descripcion, true) + '</div>';
        els.detailView.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function orderIsClosed(order) { return order && (order.estado === 'Entregada' || order.estado === 'Cancelada'); }
    function lineRows(order, kind) {
        const lines = order[kind] || []; if (!lines.length) return '<div class="empty-line">Sin líneas agregadas.</div>';
        return lines.map(function (line) { const actions = orderIsClosed(order) ? '' : '<span class="line-actions"><button type="button" class="mini-button" data-action="edit-line" data-order-id="' + escapeHtml(order.id) + '" data-kind="' + kind + '" data-id="' + escapeHtml(line.id) + '">Editar</button><button type="button" class="mini-button danger" data-action="delete-line" data-order-id="' + escapeHtml(order.id) + '" data-kind="' + kind + '" data-id="' + escapeHtml(line.id) + '">×</button></span>'; return '<div class="line-row"><div class="line-description"><strong>' + escapeHtml(line.descripcion) + '</strong>' + (line.servicioId ? '<small>Servicio del catálogo</small>' : '') + '</div><span class="line-number" data-label="Cantidad">' + escapeHtml(line.cantidad) + '</span><span class="line-number money" data-label="Unitario">' + escapeHtml(formatMoney(line.precioUnitario)) + '</span><strong class="line-number money" data-label="Subtotal">' + escapeHtml(formatMoney(line.subtotal)) + '</strong>' + actions + '</div>'; }).join('');
    }
    function partLineRows(order) {
        const lines = order.repuestos || [];
        if (!lines.length) return '<div class="empty-line">Sin repuestos agregados. El catálogo se consulta solo cuando eliges “Agregar repuesto”.</div>';
        return lines.map(function (line) {
            const snapshot = line.catalogSnapshot || {};
            const references = (snapshot.references || []).map(function (reference) {
                return '<span class="part-ref-chip' + (reference.status === 'verify' ? ' verify' : '') + '">' + escapeHtml(reference.code) + '</span>';
            }).join('');
            const links = (snapshot.links || []).slice(0, 3).map(function (link) {
                return '<a class="part-ref-chip" href="' + escapeHtml(link.url) + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(link.label || 'Fuente') + ' ↗</a>';
            }).join('');
            const compatibility = snapshot.compatibilityConfirmed
                ? 'Coincidencia confirmada con ' + (snapshot.catalogVehicleMatch || snapshot.vehicleName || 'el vehículo')
                : 'Selección desde búsqueda amplia; compatibilidad no confirmada';
            const extended = (snapshot.compatibility || []).slice(0, 2).map(function (item) { return [item.marca, item.modelos].filter(Boolean).join(': '); }).join(' · ');
            const actions = orderIsClosed(order) ? '' : '<span class="line-actions"><button type="button" class="mini-button" data-action="edit-part-line" data-order-id="' + escapeHtml(order.id) + '" data-id="' + escapeHtml(line.id) + '">Editar</button><button type="button" class="mini-button danger" data-action="delete-line" data-order-id="' + escapeHtml(order.id) + '" data-kind="repuestos" data-id="' + escapeHtml(line.id) + '">×</button></span>';
            return '<div class="part-order-row"><div class="part-order-main"><small>' + escapeHtml(snapshot.category || 'Repuesto') + '</small><strong>' + escapeHtml(snapshot.name || 'Repuesto del catálogo') + '</strong>' + (snapshot.details ? '<span class="compatibility-note">' + escapeHtml(snapshot.details) + '</span>' : '') + '<div class="part-order-meta">' + (references || '<span class="part-ref-chip verify">Sin referencia registrada</span>') + links + '</div><span class="compatibility-note">' + escapeHtml(compatibility + (extended ? ' · ' + extended : '')) + '</span></div><span class="line-number" data-label="Cantidad">' + escapeHtml(line.cantidad) + '</span><span class="line-number money" data-label="Unitario">' + (line.precioUnitario == null ? '<span class="manual-price">Precio manual pendiente</span>' : escapeHtml(formatMoney(line.precioUnitario))) + '</span><strong class="line-number money" data-label="Subtotal">' + escapeHtml(formatMoney(line.subtotal)) + '</strong>' + actions + '</div>';
        }).join('');
    }
    function totalsMarkup(totals) {
        const safe = totals || {};
        return '<div class="total-row"><span>Servicios</span><strong class="money">' + escapeHtml(formatMoney(safe.serviciosSubtotal)) + '</strong></div><div class="total-row"><span>Mano de obra</span><strong class="money">' + escapeHtml(formatMoney(safe.manoObraSubtotal)) + '</strong></div><div class="total-row"><span>Repuestos</span><strong class="money" data-total-field="parts">' + escapeHtml(formatMoney(safe.repuestosSubtotal)) + '</strong></div><div class="total-row"><span>Subtotal</span><strong class="money" data-total-field="subtotal">' + escapeHtml(formatMoney(safe.subtotal)) + '</strong></div><div class="total-row"><span>Descuento</span><strong class="money" data-total-field="discount">− ' + escapeHtml(formatMoney(safe.descuento)) + '</strong></div><div class="total-row"><span>Impuesto</span><strong class="money" data-total-field="tax">' + escapeHtml(formatMoney(safe.impuesto)) + '</strong></div><div class="total-row grand-total"><span>Total</span><strong class="money" data-total-field="total">' + escapeHtml(formatMoney(safe.total)) + '</strong></div>';
    }
    async function showOrderDetail(id) {
        const order = await repo.getWorkOrder(id); if (!order) { showToast('Orden no encontrada.'); return setSection('orders'); }
        const client = await repo.getClient(order.clienteId), vehicle = await repo.getVehicle(order.vehiculoId);
        const closed = orderIsClosed(order), disabled = closed ? ' disabled' : '';
        const editButtons = closed ? '' : '<button type="button" class="button secondary" data-action="edit-order" data-id="' + escapeHtml(id) + '">Editar datos</button>';
        const cycleButton = closed
            ? '<button type="button" class="button secondary reopen-order" data-action="reopen-order" data-id="' + escapeHtml(id) + '">Reabrir orden</button>'
            : '<button type="button" class="button close-order" data-action="close-order" data-id="' + escapeHtml(id) + '">Cerrar orden</button>';
        const addPartButton = closed ? '' : '<button type="button" class="button primary" data-action="open-part-picker" data-order-id="' + escapeHtml(id) + '">+ Agregar repuesto</button>';
        const addServiceButton = closed ? '' : '<button type="button" class="button secondary" data-action="new-line" data-order-id="' + escapeHtml(id) + '" data-kind="servicios">+ Añadir servicio</button>';
        const addLaborButton = closed ? '' : '<button type="button" class="button secondary" data-action="new-line" data-order-id="' + escapeHtml(id) + '" data-kind="manoObra">+ Añadir mano de obra</button>';
        const closedNotice = closed ? '<div class="order-closed-notice"><strong>Ciclo cerrado</strong><span>Esta orden quedó cerrada' + (order.closedAt ? ' el ' + escapeHtml(formatDate(order.closedAt)) : '') + '. Está protegida contra cambios; usa “Reabrir orden” si necesitas corregirla.</span></div>' : '';
        state.section = 'orders'; activateSectionTabs('orders'); state.detail = { kind: 'order', id: id };
        els.listView.hidden = true; els.detailView.hidden = false;
        els.detailContent.innerHTML = '<div class="print-only print-order-heading"><strong>RepuestosPro</strong><span>Orden de trabajo · ' + escapeHtml(order.identificador) + '</span></div><article class="detail-hero"><div><span class="eyebrow">' + escapeHtml(order.identificador) + ' · ' + escapeHtml(formatDate(order.fecha)) + '</span><h2>' + escapeHtml(vehicle ? vehicle.patente + ' · ' + vehicleName(vehicle) : 'Vehículo no disponible') + '</h2><p><button type="button" class="text-action" data-action="open-client" data-id="' + escapeHtml(order.clienteId) + '">' + escapeHtml(clientName(client)) + '</button> · <button type="button" class="text-action" data-action="open-vehicle" data-id="' + escapeHtml(order.vehiculoId) + '">Ver ficha del vehículo</button></p></div><div class="detail-actions"><div class="order-status-control"><label for="orderStatusSelect">Estado</label><select id="orderStatusSelect" data-order-id="' + escapeHtml(id) + '"' + disabled + '>' + statusOptions(order.estado) + '</select></div><button type="button" class="button secondary" data-action="print-order" data-id="' + escapeHtml(id) + '">Imprimir orden</button>' + cycleButton + editButtons + '</div></article>' + closedNotice +
            '<div class="order-context">' + detailField('Cliente', clientName(client)) + detailField('RUT', client && client.rut) + detailField('Teléfono', client && (client.telefono || client.whatsapp)) + detailField('Kilometraje de ingreso', formatKm(order.kilometraje)) + detailField('Estado', order.estado) + detailField('Actualizada', formatDate(order.updatedAt)) + detailField('Problema reportado', order.problemaReportado, true) + detailField('Diagnóstico', order.diagnostico, true) + detailField('Notas', order.notas, true) + '</div>' +
            '<section class="budget-panel"><div class="budget-header"><div><span class="eyebrow">PRESUPUESTO DE LA ORDEN</span><h3>Servicios, mano de obra y repuestos</h3><p>Los repuestos se guardan como instantáneas de catálogo; no existe ni se aplica movimiento de stock.</p></div>' + addPartButton + '</div>' +
            '<div class="line-section"><div class="line-section-header"><h4>Servicios</h4>' + addServiceButton + '</div><div class="line-list">' + lineRows(order, 'servicios') + '</div></div>' +
            '<div class="line-section"><div class="line-section-header"><h4>Mano de obra</h4>' + addLaborButton + '</div><div class="line-list">' + lineRows(order, 'manoObra') + '</div></div>' +
            '<div class="line-section"><div class="line-section-header"><h4>Repuestos</h4>' + addPartButton + '</div><div class="line-list">' + partLineRows(order) + '</div></div>' +
            '<div class="pricing-area"><div class="pricing-controls"><label>Descuento ($)<input id="orderDiscount" data-order-id="' + escapeHtml(id) + '" type="number" min="0" step="1" value="' + escapeHtml(order.descuento || 0) + '"' + disabled + '></label><label>Impuesto (%)<input id="orderTax" data-order-id="' + escapeHtml(id) + '" type="number" min="0" max="100" step="0.01" value="' + escapeHtml(order.impuestoPorcentaje || 0) + '"' + disabled + '></label><p class="pricing-help">El impuesto se calcula sobre el subtotal después del descuento.</p></div><div class="totals-card" id="orderTotals">' + totalsMarkup(order.totales) + '</div></div></section>';
        els.detailView.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    async function populateClientSelect(select, selectedId) {
        const clients = await repo.listClients(''); select.innerHTML = '<option value="">— Seleccionar cliente —</option>';
        clients.forEach(function (client) { const option = document.createElement('option'); option.value = client.id; option.textContent = clientName(client) + (client.rut ? ' · ' + client.rut : ''); select.appendChild(option); });
        if (selectedId) select.value = selectedId; return clients.length;
    }
    async function populateOrderVehicles(clientId, selectedId) {
        const select = els.orderForm.elements.vehiculoId, vehicles = clientId ? await repo.listVehicles('', clientId) : [];
        select.innerHTML = '<option value="">— Seleccionar vehículo —</option>';
        vehicles.forEach(function (vehicle) { const option = document.createElement('option'); option.value = vehicle.id; option.textContent = vehicle.patente + ' · ' + vehicleName(vehicle); select.appendChild(option); });
        if (selectedId) select.value = selectedId; select.disabled = !clientId; return vehicles.length;
    }
    function openDialog(dialog) { if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', ''); }
    async function openClientForm(id) {
        els.clientForm.reset(); els.clientForm.elements.id.value = ''; els.clientFormError.textContent = '';
        document.getElementById('clientDialogTitle').textContent = id ? 'Editar cliente' : 'Nuevo cliente';
        if (id) { const client = await repo.getClient(id); if (!client) return showToast('Cliente no encontrado.'); Object.keys(client).forEach(function (key) { if (els.clientForm.elements[key]) els.clientForm.elements[key].value = client[key] == null ? '' : client[key]; }); }
        openDialog(els.clientDialog); setTimeout(function () { els.clientForm.elements.nombre.focus(); }, 0);
    }
    async function openVehicleForm(id, clientId) {
        if (!(await repo.listClients('')).length) { state.pendingVehicle = true; showToast('Primero crea un cliente para asociar el vehículo.'); return openClientForm(); }
        els.vehicleForm.reset(); els.vehicleForm.elements.id.value = ''; els.vehicleFormError.textContent = '';
        document.getElementById('vehicleDialogTitle').textContent = id ? 'Editar vehículo' : 'Nuevo vehículo';
        await populateClientSelect(els.vehicleForm.elements.clienteId, clientId);
        if (id) { const vehicle = await repo.getVehicle(id); if (!vehicle) return showToast('Vehículo no encontrado.'); Object.keys(vehicle).forEach(function (key) { if (els.vehicleForm.elements[key]) els.vehicleForm.elements[key].value = vehicle[key] == null ? '' : vehicle[key]; }); }
        updateModelSuggestions(); updateYearSuggestions(); openDialog(els.vehicleDialog); setTimeout(function () { els.vehicleForm.elements.patente.focus(); }, 0);
    }
    async function openServiceForm(id) {
        els.serviceForm.reset(); els.serviceForm.elements.id.value = ''; els.serviceForm.elements.activo.checked = true; els.serviceFormError.textContent = '';
        document.getElementById('serviceDialogTitle').textContent = id ? 'Editar servicio' : 'Nuevo servicio';
        if (id) { const service = await repo.getService(id); if (!service) return showToast('Servicio no encontrado.'); Object.keys(service).forEach(function (key) { if (!els.serviceForm.elements[key]) return; if (key === 'activo') els.serviceForm.elements[key].checked = Boolean(service[key]); else els.serviceForm.elements[key].value = service[key] == null ? '' : service[key]; }); }
        openDialog(els.serviceDialog); setTimeout(function () { els.serviceForm.elements.nombre.focus(); }, 0);
    }
    async function openOrderForm(id, vehicleId) {
        if (!(await repo.listVehicles('')).length) { showToast('Primero registra un cliente y un vehículo.'); return setSection('vehicles'); }
        els.orderForm.reset(); els.orderForm.elements.id.value = ''; els.orderForm.elements.fecha.value = todayValue();
        els.orderForm.elements.estado.innerHTML = statusOptions('Presupuesto'); els.orderFormError.textContent = '';
        document.getElementById('orderDialogTitle').textContent = id ? 'Editar orden' : 'Nueva orden';
        let selectedClientId = '', selectedVehicleId = vehicleId || '', order = null;
        if (id) { order = await repo.getWorkOrder(id); if (!order) return showToast('Orden no encontrada.'); selectedClientId = order.clienteId; selectedVehicleId = order.vehiculoId; }
        else if (vehicleId) { const vehicle = await repo.getVehicle(vehicleId); selectedClientId = vehicle ? vehicle.clienteId : ''; }
        await populateClientSelect(els.orderForm.elements.clienteId, selectedClientId); await populateOrderVehicles(selectedClientId, selectedVehicleId);
        if (order) ['id', 'fecha', 'clienteId', 'vehiculoId', 'kilometraje', 'estado', 'problemaReportado', 'diagnostico', 'notas'].forEach(function (key) { if (els.orderForm.elements[key]) els.orderForm.elements[key].value = order[key] == null ? '' : order[key]; });
        openDialog(els.orderDialog); setTimeout(function () { els.orderForm.elements.problemaReportado.focus(); }, 0);
    }
    async function populateLineServices(selectedId) {
        const select = els.lineForm.elements.servicioId, services = await repo.listServices('', true);
        select.innerHTML = '<option value="">— Seleccionar servicio —</option>';
        const available = services.filter(function (service) { return service.activo || service.id === selectedId; });
        available.forEach(function (service) { const option = document.createElement('option'); option.value = service.id; option.textContent = service.nombre + ' · ' + formatMoney(service.precioBase) + (service.activo ? '' : ' (inactivo)'); select.appendChild(option); });
        if (selectedId) select.value = selectedId;
        return available.length;
    }
    async function openLineForm(orderId, kind, lineId, preferredServiceId) {
        const order = await repo.getWorkOrder(orderId); if (!order) return showToast('Orden no encontrada.');
        els.lineForm.reset(); els.lineForm.elements.orderId.value = orderId; els.lineForm.elements.kind.value = kind;
        els.lineForm.elements.id.value = ''; els.lineForm.elements.cantidad.value = '1'; els.lineFormError.textContent = '';
        const isService = kind === 'servicios'; document.getElementById('servicePickerLabel').hidden = !isService;
        document.getElementById('lineDialogTitle').textContent = (lineId ? 'Editar ' : 'Añadir ') + (isService ? 'servicio' : 'mano de obra');
        const line = lineId ? (order[kind] || []).find(function (item) { return item.id === lineId; }) : null;
        const selectedServiceId = (line && line.servicioId) || preferredServiceId || '';
        const serviceCount = await populateLineServices(selectedServiceId);
        els.servicePickerEmpty.hidden = !isService || serviceCount > 0;
        els.lineForm.elements.servicioId.disabled = isService && serviceCount === 0;
        if (line) ['id', 'servicioId', 'descripcion', 'cantidad', 'precioUnitario'].forEach(function (key) { els.lineForm.elements[key].value = line[key] == null ? '' : line[key]; });
        if (!line && preferredServiceId) {
            const service = await repo.getService(preferredServiceId);
            if (service) { els.lineForm.elements.servicioId.value = service.id; els.lineForm.elements.descripcion.value = service.nombre; els.lineForm.elements.precioUnitario.value = service.precioBase; }
        }
        openDialog(els.lineDialog); setTimeout(function () { (isService && serviceCount === 0 ? els.servicePickerEmpty.querySelector('button') : (isService ? els.lineForm.elements.servicioId : els.lineForm.elements.descripcion)).focus(); }, 0);
    }

    function renderCatalogContext(result) {
        const match = result.match || {};
        els.catalogContext.dataset.confirmed = String(Boolean(match.confirmed));
        if (match.confirmed) {
            const engineNote = match.engineProvided
                ? (match.engineMatched ? ' El motor registrado también aparece en la ficha.' : ' El motor no está confirmado de forma estructurada; revisa los detalles de la pieza.')
                : '';
            els.catalogContext.innerHTML = '<strong>Coincidencia confirmada: ' + escapeHtml(match.vehicleName) + '</strong><span>' + escapeHtml(match.reason + engineNote) + '</span>';
        } else {
            els.catalogContext.innerHTML = '<strong>Búsqueda amplia · compatibilidad no confirmada</strong><span>' + escapeHtml(match.reason || 'No fue posible confirmar el vehículo contra el catálogo.') + ' Verifica manualmente las referencias antes de usar la pieza.</span>';
        }
        els.partPickerDialog.querySelectorAll('[data-action="catalog-mode"]').forEach(function (button) {
            button.classList.toggle('active', button.dataset.mode === state.partPicker.mode);
            if (button.dataset.mode === 'compatible') button.disabled = !match.confirmed;
        });
    }

    function renderCatalogResults(result) {
        state.catalogResults = new Map(result.parts.map(function (part) { return [part.id, part]; }));
        const qualifier = result.mode === 'compatible' ? 'compatibles' : 'en búsqueda amplia';
        els.catalogResultMeta.textContent = result.total + ' resultado' + (result.total === 1 ? '' : 's') + ' ' + qualifier + (result.total > result.parts.length ? ' · mostrando ' + result.parts.length : '');
        if (!result.parts.length) {
            els.catalogResults.innerHTML = '<div class="catalog-empty">No encontramos piezas con ese texto. Prueba con el nombre del componente o una referencia sin espacios.</div>';
            return;
        }
        els.catalogResults.innerHTML = result.parts.map(function (part) {
            const refs = (part.references || []).slice(0, 4).map(function (reference) { return '<span class="part-ref-chip' + (reference.status === 'verify' ? ' verify' : '') + '">' + escapeHtml(reference.code) + '</span>'; }).join('');
            return '<button type="button" class="catalog-part-card" data-action="select-catalog-part" data-part-id="' + escapeHtml(part.id) + '"><span class="catalog-part-category">' + escapeHtml(part.category) + '</span><h3>' + escapeHtml(part.name) + '</h3>' + (part.details ? '<p>' + escapeHtml(part.details) + '</p>' : '') + '<div class="part-order-meta">' + (refs || '<span class="part-ref-chip verify">Sin referencia</span>') + '</div>' + (part.brands.length ? '<p>Marcas: ' + escapeHtml(part.brands.join(', ')) + '</p>' : '') + '<span class="catalog-part-vehicle">' + escapeHtml(part.vehicleName) + '</span></button>';
        }).join('');
    }

    async function runCatalogPartSearch() {
        if (!state.partPicker) return;
        const query = els.catalogPartSearch.value.trim();
        els.catalogResultMeta.textContent = 'Buscando…';
        try {
            const localParts = await repo.searchLocalParts(query, state.partPicker.vehicle, state.partPicker.mode);
            if (state.partPicker.mode === 'broad' && query.length < 2) {
                if (localParts.length) return renderCatalogResults({ mode: 'broad', match: state.partPicker.match, total: localParts.length, parts: localParts });
                els.catalogResultMeta.textContent = 'Escribe al menos 2 caracteres para buscar en todo el catálogo.';
                els.catalogResults.innerHTML = '<div class="catalog-empty">Los artículos locales aparecen desde el primer carácter. Para el catálogo técnico, escribe al menos 2.</div>';
                return;
            }
            const result = await CatalogAdapter.searchParts(query, {
                vehicle: state.partPicker.vehicle,
                mode: state.partPicker.mode,
                limit: 100
            });
            const seen = new Set(localParts.map(function (part) { return part.id; }));
            result.parts = localParts.concat(result.parts.filter(function (part) { return !seen.has(part.id); })).slice(0, 100);
            result.total = result.parts.length;
            state.partPicker.match = result.match;
            state.partPicker.mode = result.mode;
            renderCatalogContext(result);
            renderCatalogResults(result);
        } catch (error) {
            els.catalogResultMeta.textContent = 'No fue posible consultar el catálogo.';
            els.catalogResults.innerHTML = '<div class="catalog-empty">' + escapeHtml(error.message) + '</div>';
        }
    }

    async function openPartPicker(orderId) {
        const order = await repo.getWorkOrder(orderId);
        if (!order) return showToast('Orden no encontrada.');
        const vehicle = await repo.getVehicle(order.vehiculoId);
        if (!vehicle) return showToast('El vehículo de la orden no está disponible.');
        state.partPicker = { orderId: orderId, vehicle: vehicle, mode: 'compatible', match: null };
        state.catalogResults = new Map();
        els.catalogPartSearch.value = '';
        els.catalogContext.removeAttribute('data-confirmed');
        els.catalogContext.innerHTML = '<strong>Buscando coincidencia para ' + escapeHtml(vehicle.patente + ' · ' + vehicleName(vehicle)) + '…</strong><span>Los datos pesados se cargan ahora y permanecerán en memoria durante esta sesión.</span>';
        els.catalogResultMeta.textContent = 'Cargando catálogo…';
        els.catalogResults.innerHTML = '<div class="catalog-empty">Preparando piezas compatibles…</div>';
        openDialog(els.partPickerDialog);
        try {
            const result = await CatalogAdapter.findCompatibleParts(vehicle);
            state.partPicker.match = result.match;
            state.partPicker.mode = result.match.confirmed ? 'compatible' : 'broad';
            renderCatalogContext(result);
            if (state.partPicker.mode === 'broad') await runCatalogPartSearch();
            else renderCatalogResults({ mode: 'compatible', match: result.match, total: result.parts.length, parts: result.parts.slice(0, 100) });
        } catch (error) {
            els.catalogResultMeta.textContent = 'No fue posible cargar el catálogo.';
            els.catalogResults.innerHTML = '<div class="catalog-empty">' + escapeHtml(error.message) + '</div>';
        }
    }

    function renderSelectedPart(snapshot) {
        const references = (snapshot.references || []).map(function (reference) { return '<span class="part-ref-chip' + (reference.status === 'verify' ? ' verify' : '') + '">' + escapeHtml(reference.code) + '</span>'; }).join('');
        els.selectedPartSummary.innerHTML = '<h3>' + escapeHtml(snapshot.name || 'Repuesto del catálogo') + '</h3><p>' + escapeHtml([snapshot.category, snapshot.vehicleName].filter(Boolean).join(' · ')) + '</p><div class="part-order-meta">' + (references || '<span class="part-ref-chip verify">Sin referencia registrada</span>') + '</div><p>' + escapeHtml(snapshot.compatibilityConfirmed ? 'Compatibilidad contextual confirmada.' : 'Búsqueda amplia: compatibilidad no confirmada.') + '</p>';
    }

    async function openPartLineForm(orderId, lineId, part) {
        const order = await repo.getWorkOrder(orderId);
        if (!order) return showToast('Orden no encontrada.');
        let line = null;
        if (lineId) line = (order.repuestos || []).find(function (item) { return item.id === lineId; });
        const snapshot = line ? line.catalogSnapshot : Object.assign({}, part, { capturedAt: new Date().toISOString() });
        if (!snapshot) return showToast('Selecciona un repuesto del catálogo.');
        state.selectedCatalogPart = snapshot;
        els.partLineForm.reset();
        els.partLineForm.elements.orderId.value = orderId;
        els.partLineForm.elements.id.value = line ? line.id : '';
        els.partLineForm.elements.cantidad.value = line ? line.cantidad : '1';
        els.partLineForm.elements.precioUnitario.value = line && line.precioUnitario != null ? line.precioUnitario : '';
        els.partLineFormError.textContent = '';
        document.getElementById('partLineTitle').textContent = line ? 'Editar repuesto' : 'Agregar repuesto';
        renderSelectedPart(snapshot);
        openDialog(els.partLineDialog);
        setTimeout(function () { els.partLineForm.elements.cantidad.focus(); }, 0);
    }

    async function openManualPartForm() {
        if (!state.partPicker) return showToast('Abre una orden y selecciona agregar repuesto.');
        const vehicle = state.partPicker.vehicle;
        els.manualPartForm.reset();
        els.manualPartForm.elements.orderId.value = state.partPicker.orderId;
        els.manualPartVehicle.textContent = 'Vehículo asociado: ' + vehicleName(vehicle) + (vehicle.motor ? ' · Motor ' + vehicle.motor : '');
        els.manualPartFormError.textContent = '';
        els.partPickerDialog.close();
        openDialog(els.manualPartDialog);
        setTimeout(function () { els.manualPartForm.elements.name.focus(); }, 0);
    }

    async function saveManualPart(event) {
        event.preventDefault();
        els.manualPartFormError.textContent = '';
        const data = formObject(els.manualPartForm);
        if (!data.name.trim()) return showError(els.manualPartFormError, 'El nombre del repuesto es obligatorio.');
        const order = await repo.getWorkOrder(data.orderId);
        const vehicle = order ? await repo.getVehicle(order.vehiculoId) : null;
        if (!order || !vehicle) return showError(els.manualPartFormError, 'La orden o su vehículo ya no están disponibles.');
        try {
            const pending = await repo.queuePendingPart({ name: data.name, brand: data.brand, reference: data.reference, notes: data.notes, vehicle: vehicle });
            const snapshot = {
                id: 'local-' + pending.id, pendingResearchId: pending.id, name: pending.name,
                category: 'Repuesto nuevo', details: pending.notes, brands: pending.brand ? [pending.brand] : [],
                references: pending.reference ? [{ code: pending.reference, status: 'verify' }] : [],
                compatibility: [{ marca: pending.vehicle.marca, modelos: [pending.vehicle.modelo, pending.vehicle.anio].filter(Boolean).join(' ') }],
                compatibilityConfirmed: false, matchMode: 'broad',
                vehicleName: [pending.vehicle.marca, pending.vehicle.modelo, pending.vehicle.anio].filter(Boolean).join(' '),
                capturedAt: new Date().toISOString()
            };
            els.manualPartDialog.close();
            showToast('Repuesto guardado como pendiente de investigación.');
            await openPartLineForm(data.orderId, null, snapshot);
        } catch (error) { showError(els.manualPartFormError, error); }
    }

    async function openPendingParts() {
        const items = await repo.listPendingParts();
        const pending = items.filter(function (item) { return item.status === 'pending'; }).length;
        const enriched = items.filter(function (item) { return item.status === 'enriched'; }).length;
        els.pendingPartsMeta.textContent = pending + ' pendiente' + (pending === 1 ? '' : 's') + ' · ' + enriched + ' enriquecido' + (enriched === 1 ? '' : 's');
        els.pendingPartsList.innerHTML = items.length ? items.map(function (item) {
            const vehicle = [item.vehicle.marca, item.vehicle.modelo, item.vehicle.anio, item.vehicle.motor].filter(Boolean).join(' · ');
            const label = item.status === 'enriched' ? 'Enriquecido' : (item.status === 'rejected' ? 'Descartado' : 'Pendiente');
            return '<article class="catalog-part-card pending-part-card"><span class="catalog-part-category">' + escapeHtml(label) + '</span><h3>' + escapeHtml(item.name) + '</h3><p>' + escapeHtml([item.brand, item.reference].filter(Boolean).join(' · ') || 'Sin marca ni referencia') + '</p><span class="catalog-part-vehicle">' + escapeHtml(vehicle || 'Vehículo sin detalle') + '</span>' + (item.occurrences > 1 ? '<p>Registrado ' + escapeHtml(item.occurrences) + ' veces</p>' : '') + '</article>';
        }).join('') : '<div class="catalog-empty">Todavía no hay artículos nuevos pendientes.</div>';
        openDialog(els.pendingPartsDialog);
    }

    function downloadJson(filename, payload) {
        const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob), link = document.createElement('a');
        link.href = url; link.download = filename; document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(url);
    }

    async function exportPendingParts() {
        const batch = await repo.exportPendingParts();
        if (!batch.items.length) return showToast('No hay artículos pendientes para exportar.');
        downloadJson('repuestospro-enrichment-batch-' + batch.createdAt.slice(0, 10) + '.json', batch);
        showToast('Lote técnico exportado sin datos de clientes.');
    }

    async function importEnrichmentFile(file) {
        try {
            const payload = JSON.parse(await file.text());
            const result = await repo.importEnrichmentPackage(payload);
            showToast(result.updated + ' artículo' + (result.updated === 1 ? '' : 's') + ' actualizado' + (result.updated === 1 ? '' : 's') + '.');
            await openPendingParts();
        } catch (error) { showToast(error.message); }
    }

    function formObject(form) { return Object.fromEntries(new FormData(form).entries()); }
    function validRut(rut) {
        const normalized = TallerData.normalizeRut(rut).replace('-', ''); if (!/^\d{7,8}[0-9K]$/.test(normalized)) return false;
        const body = normalized.slice(0, -1), verifier = normalized.slice(-1); let sum = 0, multiplier = 2;
        for (let index = body.length - 1; index >= 0; index -= 1) { sum += Number(body[index]) * multiplier; multiplier = multiplier === 7 ? 2 : multiplier + 1; }
        const result = 11 - (sum % 11), expected = result === 11 ? '0' : (result === 10 ? 'K' : String(result)); return verifier === expected;
    }
    async function saveClient(event) {
        event.preventDefault(); els.clientFormError.textContent = ''; const data = formObject(els.clientForm), id = data.id;
        if (!data.nombre.trim() || !data.apellido.trim() || !data.rut.trim()) return showError(els.clientFormError, 'Nombre, apellido y RUT son obligatorios.');
        if (!validRut(data.rut)) return showError(els.clientFormError, 'Ingresa un RUT chileno válido.');
        if (!(await repo.isRutAvailable(data.rut, id))) return showError(els.clientFormError, 'Ya existe un cliente con ese RUT.');
        if (data.email && !els.clientForm.elements.email.validity.valid) return showError(els.clientFormError, 'Ingresa un email válido.');
        try { const saved = id ? await repo.updateClient(id, data) : await repo.createClient(data); els.clientDialog.close(); await refreshSummary(); await renderList(); showToast(id ? 'Cliente actualizado.' : 'Cliente creado.'); if (state.pendingVehicle) { state.pendingVehicle = false; await openVehicleForm(null, saved.id); } else if (id && state.detail && state.detail.kind === 'client') await showClientDetail(saved.id); } catch (error) { showError(els.clientFormError, error); }
    }
    async function saveVehicle(event) {
        event.preventDefault(); els.vehicleFormError.textContent = ''; const data = formObject(els.vehicleForm), id = data.id, plate = TallerData.normalizePlate(data.patente), currentYear = new Date().getFullYear() + 1;
        if (!data.clienteId || !plate || !data.marca.trim() || !data.modelo.trim() || !data.anio) return showError(els.vehicleFormError, 'Cliente, patente, marca, modelo y año son obligatorios.');
        if (!/^[A-Z0-9]{4,8}$/.test(plate)) return showError(els.vehicleFormError, 'La patente debe tener entre 4 y 8 letras o números.');
        if (!(await repo.isPlateAvailable(plate, id))) return showError(els.vehicleFormError, 'Ya existe un vehículo con esa patente.');
        if (data.vin && !/^[A-HJ-NPR-Z0-9]{17}$/i.test(data.vin.trim())) return showError(els.vehicleFormError, 'El VIN debe tener 17 caracteres y no usar I, O o Q.');
        if (!(await repo.isVinAvailable(data.vin, id))) return showError(els.vehicleFormError, 'Ya existe un vehículo con ese VIN.');
        const year = Number(data.anio); if (!Number.isInteger(year) || year < 1900 || year > currentYear) return showError(els.vehicleFormError, 'El año debe estar entre 1900 y ' + currentYear + '.');
        if (data.kilometraje && Number(data.kilometraje) < 0) return showError(els.vehicleFormError, 'El kilometraje no puede ser negativo.');
        if (!(await repo.getClient(data.clienteId))) return showError(els.vehicleFormError, 'Selecciona un cliente existente.');
        try { data.patente = plate; const saved = id ? await repo.updateVehicle(id, data) : await repo.createVehicle(data); els.vehicleDialog.close(); await refreshSummary(); await renderList(); showToast(id ? 'Vehículo actualizado.' : 'Vehículo registrado.'); await showVehicleDetail(saved.id); } catch (error) { showError(els.vehicleFormError, error); }
    }
    async function saveService(event) {
        event.preventDefault(); els.serviceFormError.textContent = ''; const data = formObject(els.serviceForm); data.activo = els.serviceForm.elements.activo.checked;
        if (!data.nombre.trim()) return showError(els.serviceFormError, 'El nombre es obligatorio.');
        if (data.precioBase === '' || Number(data.precioBase) < 0) return showError(els.serviceFormError, 'El precio base debe ser cero o mayor.');
        if (data.duracionEstimada && Number(data.duracionEstimada) < 0) return showError(els.serviceFormError, 'La duración no puede ser negativa.');
        try {
            const saved = data.id ? await repo.updateService(data.id, data) : await repo.createService(data);
            const pendingLine = state.pendingLineAfterService; state.pendingLineAfterService = null;
            els.serviceDialog.close(); await refreshSummary();
            if (pendingLine) {
                showToast('Servicio creado y disponible en el presupuesto.');
                await showOrderDetail(pendingLine.orderId);
                return openLineForm(pendingLine.orderId, pendingLine.kind, pendingLine.lineId, saved.id);
            }
            await renderList(); showToast(data.id ? 'Servicio actualizado.' : 'Servicio creado.'); await showServiceDetail(saved.id);
        } catch (error) { showError(els.serviceFormError, error); }
    }
    async function saveOrder(event) {
        event.preventDefault(); els.orderFormError.textContent = ''; const data = formObject(els.orderForm);
        if (!data.fecha || !data.clienteId || !data.vehiculoId || !data.problemaReportado.trim()) return showError(els.orderFormError, 'Fecha, cliente, vehículo y problema reportado son obligatorios.');
        if (data.kilometraje && Number(data.kilometraje) < 0) return showError(els.orderFormError, 'El kilometraje no puede ser negativo.');
        try { const saved = data.id ? await repo.updateWorkOrder(data.id, data) : await repo.createWorkOrder(data); els.orderDialog.close(); await refreshSummary(); await renderList(); showToast(data.id ? 'Orden actualizada.' : 'Orden creada.'); await showOrderDetail(saved.id); } catch (error) { showError(els.orderFormError, error); }
    }
    async function saveLine(event) {
        event.preventDefault(); els.lineFormError.textContent = ''; const data = formObject(els.lineForm);
        if (!data.descripcion.trim()) return showError(els.lineFormError, 'La descripción es obligatoria.');
        if (!(Number(data.cantidad) > 0)) return showError(els.lineFormError, 'La cantidad debe ser mayor que cero.');
        if (data.precioUnitario === '' || Number(data.precioUnitario) < 0) return showError(els.lineFormError, 'El precio unitario debe ser cero o mayor.');
        try { await repo.saveOrderLine(data.orderId, data.kind, data); els.lineDialog.close(); showToast(data.id ? 'Línea actualizada.' : 'Línea añadida.'); await showOrderDetail(data.orderId); } catch (error) { showError(els.lineFormError, error); }
    }
    async function savePartLine(event) {
        event.preventDefault();
        els.partLineFormError.textContent = '';
        const data = formObject(els.partLineForm);
        if (!(Number(data.cantidad) > 0)) return showError(els.partLineFormError, 'La cantidad debe ser mayor que cero.');
        if (data.precioUnitario !== '' && Number(data.precioUnitario) < 0) return showError(els.partLineFormError, 'El precio unitario debe ser cero o mayor.');
        if (!state.selectedCatalogPart) return showError(els.partLineFormError, 'No hay una pieza de catálogo seleccionada.');
        try {
            await repo.saveOrderLine(data.orderId, 'repuestos', {
                id: data.id,
                cantidad: data.cantidad,
                precioUnitario: data.precioUnitario,
                catalogSnapshot: state.selectedCatalogPart
            });
            els.partLineDialog.close();
            showToast(data.id ? 'Repuesto actualizado.' : 'Repuesto agregado sin movimiento de stock.');
            await showOrderDetail(data.orderId);
        } catch (error) { showError(els.partLineFormError, error); }
    }

    async function deleteClient(id) { const client = await repo.getClient(id); if (!client || !window.confirm('¿Eliminar a ' + clientName(client) + '? Esta acción no se puede deshacer.')) return; try { await repo.deleteClient(id); await refreshSummary(); showToast('Cliente eliminado.'); await setSection('clients'); } catch (error) { showToast(error.message); } }
    async function deleteVehicle(id) { const vehicle = await repo.getVehicle(id); if (!vehicle || !window.confirm('¿Eliminar el vehículo patente ' + vehicle.patente + '? Esta acción no se puede deshacer.')) return; try { await repo.deleteVehicle(id); await refreshSummary(); showToast('Vehículo eliminado.'); await setSection('vehicles'); } catch (error) { showToast(error.message); } }
    async function deleteService(id) { const service = await repo.getService(id); if (!service || !window.confirm('¿Eliminar el servicio “' + service.nombre + '”? Las líneas ya guardadas en órdenes se conservarán.')) return; try { await repo.deleteService(id); await refreshSummary(); showToast('Servicio eliminado.'); await setSection('services'); } catch (error) { showToast(error.message); } }
    async function deleteLine(target) { if (!window.confirm('¿Eliminar esta línea del presupuesto?')) return; try { await repo.deleteOrderLine(target.dataset.orderId, target.dataset.kind, target.dataset.id); showToast('Línea eliminada.'); await showOrderDetail(target.dataset.orderId); } catch (error) { showToast(error.message); } }
    async function handleAction(action, target) {
        const id = target.dataset.id;
        if (action === 'show-onboarding') return showOnboarding();
        if (action === 'dismiss-onboarding') { setOnboardingDismissed(true); els.onboardingPanel.hidden = true; return; }
        if (action === 'export-backup') return exportBackup();
        if (action === 'new-manual-part') return openManualPartForm();
        if (action === 'open-pending-parts') return openPendingParts();
        if (action === 'export-pending-parts') return exportPendingParts();
        if (action === 'import-enrichment') { els.enrichmentFileInput.value = ''; els.enrichmentFileInput.click(); return; }
        if (action === 'create-service-from-line') {
            state.pendingLineAfterService = {
                orderId: els.lineForm.elements.orderId.value,
                kind: els.lineForm.elements.kind.value,
                lineId: els.lineForm.elements.id.value || null
            };
            els.lineDialog.close(); return openServiceForm();
        }
        if (action === 'new-client') return openClientForm(); if (action === 'new-vehicle') return openVehicleForm(null, target.dataset.clientId);
        if (action === 'new-service') return openServiceForm(); if (action === 'new-order') return openOrderForm(null, target.dataset.vehicleId);
        if (action === 'new-line') return openLineForm(target.dataset.orderId, target.dataset.kind); if (action === 'edit-client') return openClientForm(id);
        if (action === 'open-part-picker') return openPartPicker(target.dataset.orderId);
        if (action === 'select-catalog-part') {
            const part = state.catalogResults.get(target.dataset.partId);
            if (!part || !state.partPicker) return showToast('El resultado de catálogo ya no está disponible.');
            els.partPickerDialog.close();
            return openPartLineForm(state.partPicker.orderId, null, part);
        }
        if (action === 'catalog-mode') {
            if (!state.partPicker) return;
            state.partPicker.mode = target.dataset.mode;
            return runCatalogPartSearch();
        }
        if (action === 'edit-vehicle') return openVehicleForm(id); if (action === 'edit-service') return openServiceForm(id);
        if (action === 'edit-order') return openOrderForm(id); if (action === 'edit-line') return openLineForm(target.dataset.orderId, target.dataset.kind, id);
        if (action === 'edit-part-line') return openPartLineForm(target.dataset.orderId, id);
        if (action === 'delete-client') return deleteClient(id); if (action === 'delete-vehicle') return deleteVehicle(id);
        if (action === 'delete-service') return deleteService(id); if (action === 'delete-line') return deleteLine(target);
        if (action === 'open-client') return showClientDetail(id); if (action === 'open-vehicle') return showVehicleDetail(id);
        if (action === 'close-order') return closeOrder(id); if (action === 'reopen-order') return reopenOrder(id);
        if (action === 'print-order') return printOrder(id);
        if (action === 'open-order') return showOrderDetail(id); if (action === 'back-to-list') return setSection(state.section);
    }
    async function closeOrder(id) {
        if (!window.confirm('¿Cerrar esta orden de trabajo? Quedará marcada como entregada y bloqueada contra cambios.')) return;
        try { await repo.closeWorkOrder(id); showToast('Orden cerrada. El ciclo quedó finalizado.'); await refreshSummary(); await showOrderDetail(id); } catch (error) { showToast(error.message); }
    }
    async function reopenOrder(id) {
        try { await repo.reopenWorkOrder(id); showToast('Orden reabierta. Ya puedes editarla.'); await refreshSummary(); await showOrderDetail(id); } catch (error) { showToast(error.message); }
    }
    async function printOrder(id) {
        const order = await repo.getWorkOrder(id); if (!order) return showToast('Orden no encontrada.');
        const previousTitle = document.title;
        document.title = order.identificador + ' - Orden de trabajo';
        window.addEventListener('afterprint', function restoreTitle() { document.title = previousTitle; }, { once: true });
        window.print();
    }
    async function exportBackup() {
        try {
            const backup = await repo.createBackup();
            const date = backup.createdAt.slice(0, 10);
            const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob), link = document.createElement('a');
            link.href = url; link.download = 'repuestospro-taller-backup-' + date + '.json';
            document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(url);
            showToast('Respaldo verificable descargado. Guárdalo en un lugar seguro.');
        } catch (error) { showToast(error.message); }
    }
    async function handleStatusChange(select) { try { await repo.setWorkOrderStatus(select.dataset.orderId, select.value); showToast('Estado actualizado a ' + select.value + '.'); await showOrderDetail(select.dataset.orderId); } catch (error) { showToast(error.message); } }
    async function previewAndSavePricing(input) {
        const orderId = input.dataset.orderId, discountInput = document.getElementById('orderDiscount'), taxInput = document.getElementById('orderTax'); if (!discountInput || !taxInput) return;
        const order = await repo.getWorkOrder(orderId); if (!order) return;
        const subtotal = Number(order.totales.subtotal) || 0, discount = Math.min(Math.max(Number(discountInput.value) || 0, 0), subtotal), taxable = subtotal - discount;
        const taxPercent = Math.min(Math.max(Number(taxInput.value) || 0, 0), 100), tax = Math.round(taxable * taxPercent) / 100;
        els.detailContent.querySelectorAll('[data-total-field]').forEach(function (field) { if (field.dataset.totalField === 'discount') field.textContent = '− ' + formatMoney(discount); if (field.dataset.totalField === 'tax') field.textContent = formatMoney(tax); if (field.dataset.totalField === 'total') field.textContent = formatMoney(taxable + tax); });
        clearTimeout(state.pricingTimer); state.pricingTimer = setTimeout(async function () { try { await repo.updateOrderPricing(orderId, discountInput.value, taxInput.value); showToast('Totales guardados.'); } catch (error) { showToast(error.message); } }, 250);
    }

    document.addEventListener('click', function (event) {
        const actionTarget = event.target.closest('[data-action]'); if (actionTarget) return void handleAction(actionTarget.dataset.action, actionTarget);
        const card = event.target.closest('.record-card[data-kind]');
        if (card) { if (card.dataset.kind === 'client') return void showClientDetail(card.dataset.id); if (card.dataset.kind === 'vehicle') return void showVehicleDetail(card.dataset.id); if (card.dataset.kind === 'order') return void showOrderDetail(card.dataset.id); if (card.dataset.kind === 'service') return void showServiceDetail(card.dataset.id); }
        const close = event.target.closest('[data-close-dialog]'); if (close) close.closest('dialog').close();
    });
    document.addEventListener('change', function (event) { if (event.target.id === 'orderStatusSelect') handleStatusChange(event.target); });
    document.addEventListener('input', function (event) { if (event.target.id === 'orderDiscount' || event.target.id === 'orderTax') previewAndSavePricing(event.target); });
    [els.clientDialog, els.vehicleDialog, els.serviceDialog, els.orderDialog, els.lineDialog, els.partPickerDialog, els.partLineDialog, els.manualPartDialog, els.pendingPartsDialog].forEach(function (dialog) { dialog.addEventListener('click', function (event) { if (event.target === dialog) dialog.close(); }); });
    els.serviceDialog.addEventListener('close', function () {
        if (!state.pendingLineAfterService) return;
        const pendingLine = state.pendingLineAfterService; state.pendingLineAfterService = null;
        openLineForm(pendingLine.orderId, pendingLine.kind, pendingLine.lineId);
    });
    Object.keys(tabs).forEach(function (section) { tabs[section].addEventListener('click', function () { setSection(section); }); });
    els.addRecordButton.addEventListener('click', function () { if (state.section === 'clients') openClientForm(); if (state.section === 'vehicles') openVehicleForm(); if (state.section === 'orders') openOrderForm(); if (state.section === 'services') openServiceForm(); });
    els.recordSearch.addEventListener('input', function () { state.query = els.recordSearch.value.trim(); renderList(); });
    els.vehicleForm.elements.marca.addEventListener('input', updateModelSuggestions); els.vehicleForm.elements.modelo.addEventListener('input', updateYearSuggestions);
    els.orderForm.elements.clienteId.addEventListener('change', function () { populateOrderVehicles(els.orderForm.elements.clienteId.value); });
    els.lineForm.elements.servicioId.addEventListener('change', async function () { const service = await repo.getService(els.lineForm.elements.servicioId.value); if (!service) return; els.lineForm.elements.descripcion.value = service.nombre; els.lineForm.elements.precioUnitario.value = service.precioBase; });
    els.clientForm.addEventListener('submit', saveClient); els.vehicleForm.addEventListener('submit', saveVehicle); els.serviceForm.addEventListener('submit', saveService); els.orderForm.addEventListener('submit', saveOrder); els.lineForm.addEventListener('submit', saveLine); els.partLineForm.addEventListener('submit', savePartLine); els.manualPartForm.addEventListener('submit', saveManualPart);
    els.enrichmentFileInput.addEventListener('change', function () { if (els.enrichmentFileInput.files[0]) importEnrichmentFile(els.enrichmentFileInput.files[0]); });
    els.catalogPartSearch.addEventListener('input', function () {
        clearTimeout(state.catalogSearchTimer);
        state.catalogSearchTimer = setTimeout(runCatalogPartSearch, 180);
    });
    els.plateSearch.addEventListener('input', function () { els.plateSearch.value = els.plateSearch.value.toUpperCase(); els.plateSearchMessage.textContent = ''; });
    els.paletteButton.addEventListener('click', function (event) { event.stopPropagation(); const opening = els.palettePopover.hidden; els.palettePopover.hidden = !opening; els.paletteButton.setAttribute('aria-expanded', String(opening)); });
    els.paletteRange.addEventListener('input', function () { const appearance = readAppearance(); appearance.palette = ['navy','copper','sage','wine','electric','teal','amber','violet'][Number(els.paletteRange.value)]; applyAppearance(appearance); });
    document.addEventListener('click', function (event) { if (!event.target.closest('.color-picker')) { els.palettePopover.hidden = true; els.paletteButton.setAttribute('aria-expanded', 'false'); } });
    els.themeToggle.addEventListener('click', cycleTheme);
    els.plateSearchForm.addEventListener('submit', async function (event) { event.preventDefault(); const plate = TallerData.normalizePlate(els.plateSearch.value); if (!plate) { els.plateSearchMessage.textContent = 'Escribe una patente para buscar.'; return; } const vehicle = await repo.findVehicleByPlate(plate); if (!vehicle) { els.plateSearchMessage.textContent = 'No hay un vehículo registrado con esa patente.'; return; } els.plateSearchMessage.textContent = ''; await showVehicleDetail(vehicle.id); });
    els.compactPlateSearchForm.addEventListener('submit', async function (event) { event.preventDefault(); const plate = TallerData.normalizePlate(els.compactPlateSearch.value); if (!plate) { els.compactPlateSearchMessage.textContent = 'Escribe una patente.'; return; } const vehicle = await repo.findVehicleByPlate(plate); if (!vehicle) { els.compactPlateSearchMessage.textContent = 'Patente no encontrada.'; return; } els.compactPlateSearchMessage.textContent = ''; await showVehicleDetail(vehicle.id); });

    applyAppearance(readAppearance());
    TallerData.SyncedWorkshopRepository.create().catch(function () {
        return new TallerData.LocalWorkshopRepository();
    }).then(function (repository) {
        repo = repository;
        return Promise.all([loadCatalogNavigation(), refreshSummary()]);
    }).then(function () { return renderList(); }).catch(function (error) { els.recordList.innerHTML = '<div class="empty-state"><strong>No pudimos abrir los datos del taller</strong><p>' + escapeHtml(error.message) + '</p></div>'; });
})();
