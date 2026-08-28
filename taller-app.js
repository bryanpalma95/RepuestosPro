(function () {
    'use strict';

    const repo = new TallerData.LocalWorkshopRepository();
    const state = {
        section: 'clients', query: '', catalog: {}, detail: null, pendingVehicle: false,
        pricingTimer: null, catalogSearchTimer: null, partPicker: null, catalogResults: new Map(), selectedCatalogPart: null
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
        partLineDialog: document.getElementById('partLineDialog'), clientForm: document.getElementById('clientForm'),
        vehicleForm: document.getElementById('vehicleForm'), serviceForm: document.getElementById('serviceForm'),
        orderForm: document.getElementById('orderForm'), lineForm: document.getElementById('lineForm'),
        partLineForm: document.getElementById('partLineForm'),
        clientFormError: document.getElementById('clientFormError'), vehicleFormError: document.getElementById('vehicleFormError'),
        serviceFormError: document.getElementById('serviceFormError'), orderFormError: document.getElementById('orderFormError'),
        lineFormError: document.getElementById('lineFormError'), partLineFormError: document.getElementById('partLineFormError'),
        catalogContext: document.getElementById('catalogContext'), catalogPartSearch: document.getElementById('catalogPartSearch'),
        catalogResultMeta: document.getElementById('catalogResultMeta'), catalogResults: document.getElementById('catalogResults'),
        selectedPartSummary: document.getElementById('selectedPartSummary'), plateSearchForm: document.getElementById('plateSearchForm'),
        plateSearch: document.getElementById('plateSearch'), plateSearchMessage: document.getElementById('plateSearchMessage'),
        toast: document.getElementById('toast')
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
    async function refreshSummary() {
        const summary = await repo.getSummary();
        els.clientCount.textContent = summary.clients; els.vehicleCount.textContent = summary.vehicles;
        els.orderCount.textContent = summary.workOrders; els.serviceCount.textContent = summary.activeServices;
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
        let records = [], clients = [], vehicles = [];
        if (state.section === 'clients') records = await repo.listClients(state.query);
        if (state.section === 'vehicles') { records = await repo.listVehicles(state.query); clients = await repo.listClients(''); }
        if (state.section === 'orders') { records = await repo.listWorkOrders(state.query); clients = await repo.listClients(''); vehicles = await repo.listVehicles(''); }
        if (state.section === 'services') records = await repo.listServices(state.query, true);
        const clientsById = new Map(clients.map(function (client) { return [client.id, client]; }));
        const vehiclesById = new Map(vehicles.map(function (vehicle) { return [vehicle.id, vehicle]; }));
        els.workspaceTitle.textContent = copy.title; els.workspaceEyebrow.textContent = copy.eyebrow;
        els.addRecordButton.textContent = copy.add; els.recordSearch.placeholder = copy.placeholder;
        els.resultCount.textContent = records.length + ' registro' + (records.length === 1 ? '' : 's');
        if (!records.length) { els.recordList.innerHTML = emptyState(state.section, Boolean(state.query)); return; }
        els.recordList.innerHTML = records.map(function (record) {
            if (state.section === 'clients') {
                const contact = record.whatsapp || record.telefono || record.email || 'Sin contacto registrado';
                return '<button type="button" class="record-card" data-kind="client" data-id="' + escapeHtml(record.id) + '"><span class="record-id">' + valueOrDash(record.rut) + '</span><h3>' + escapeHtml(clientName(record)) + '</h3><p>' + escapeHtml(contact) + '</p><p>' + valueOrDash(record.direccion) + '</p></button>';
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
            '<div class="detail-grid">' + detailField('Patente', vehicle.patente) + detailField('VIN', vehicle.vin) + detailField('Cliente', clientName(client)) + detailField('Marca', vehicle.marca) + detailField('Modelo', vehicle.modelo) + detailField('Año', vehicle.anio) + detailField('Motor', vehicle.motor) + detailField('Cilindrada', vehicle.cilindrada) + detailField('Combustible', vehicle.combustible) + detailField('Transmisión', vehicle.transmision) + detailField('Kilometraje', formatKm(vehicle.kilometraje)) + detailField('Color', vehicle.color) + detailField('Notas', vehicle.notas, true) + '</div>' +
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

    function lineRows(order, kind) {
        const lines = order[kind] || []; if (!lines.length) return '<div class="empty-line">Sin líneas agregadas.</div>';
        return lines.map(function (line) { return '<div class="line-row"><div class="line-description"><strong>' + escapeHtml(line.descripcion) + '</strong>' + (line.servicioId ? '<small>Servicio del catálogo</small>' : '') + '</div><span class="line-number" data-label="Cantidad">' + escapeHtml(line.cantidad) + '</span><span class="line-number money" data-label="Unitario">' + escapeHtml(formatMoney(line.precioUnitario)) + '</span><strong class="line-number money" data-label="Subtotal">' + escapeHtml(formatMoney(line.subtotal)) + '</strong><span class="line-actions"><button type="button" class="mini-button" data-action="edit-line" data-order-id="' + escapeHtml(order.id) + '" data-kind="' + kind + '" data-id="' + escapeHtml(line.id) + '">Editar</button><button type="button" class="mini-button danger" data-action="delete-line" data-order-id="' + escapeHtml(order.id) + '" data-kind="' + kind + '" data-id="' + escapeHtml(line.id) + '">×</button></span></div>'; }).join('');
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
            return '<div class="part-order-row"><div class="part-order-main"><small>' + escapeHtml(snapshot.category || 'Repuesto') + '</small><strong>' + escapeHtml(snapshot.name || 'Repuesto del catálogo') + '</strong>' + (snapshot.details ? '<span class="compatibility-note">' + escapeHtml(snapshot.details) + '</span>' : '') + '<div class="part-order-meta">' + (references || '<span class="part-ref-chip verify">Sin referencia registrada</span>') + links + '</div><span class="compatibility-note">' + escapeHtml(compatibility + (extended ? ' · ' + extended : '')) + '</span></div><span class="line-number" data-label="Cantidad">' + escapeHtml(line.cantidad) + '</span><span class="line-number money" data-label="Unitario">' + (line.precioUnitario == null ? '<span class="manual-price">Precio manual pendiente</span>' : escapeHtml(formatMoney(line.precioUnitario))) + '</span><strong class="line-number money" data-label="Subtotal">' + escapeHtml(formatMoney(line.subtotal)) + '</strong><span class="line-actions"><button type="button" class="mini-button" data-action="edit-part-line" data-order-id="' + escapeHtml(order.id) + '" data-id="' + escapeHtml(line.id) + '">Editar</button><button type="button" class="mini-button danger" data-action="delete-line" data-order-id="' + escapeHtml(order.id) + '" data-kind="repuestos" data-id="' + escapeHtml(line.id) + '">×</button></span></div>';
        }).join('');
    }
    function totalsMarkup(totals) {
        const safe = totals || {};
        return '<div class="total-row"><span>Servicios</span><strong class="money">' + escapeHtml(formatMoney(safe.serviciosSubtotal)) + '</strong></div><div class="total-row"><span>Mano de obra</span><strong class="money">' + escapeHtml(formatMoney(safe.manoObraSubtotal)) + '</strong></div><div class="total-row"><span>Repuestos</span><strong class="money" data-total-field="parts">' + escapeHtml(formatMoney(safe.repuestosSubtotal)) + '</strong></div><div class="total-row"><span>Subtotal</span><strong class="money" data-total-field="subtotal">' + escapeHtml(formatMoney(safe.subtotal)) + '</strong></div><div class="total-row"><span>Descuento</span><strong class="money" data-total-field="discount">− ' + escapeHtml(formatMoney(safe.descuento)) + '</strong></div><div class="total-row"><span>Impuesto</span><strong class="money" data-total-field="tax">' + escapeHtml(formatMoney(safe.impuesto)) + '</strong></div><div class="total-row grand-total"><span>Total</span><strong class="money" data-total-field="total">' + escapeHtml(formatMoney(safe.total)) + '</strong></div>';
    }
    async function showOrderDetail(id) {
        const order = await repo.getWorkOrder(id); if (!order) { showToast('Orden no encontrada.'); return setSection('orders'); }
        const client = await repo.getClient(order.clienteId), vehicle = await repo.getVehicle(order.vehiculoId);
        state.section = 'orders'; activateSectionTabs('orders'); state.detail = { kind: 'order', id: id };
        els.listView.hidden = true; els.detailView.hidden = false;
        els.detailContent.innerHTML = '<article class="detail-hero"><div><span class="eyebrow">' + escapeHtml(order.identificador) + ' · ' + escapeHtml(formatDate(order.fecha)) + '</span><h2>' + escapeHtml(vehicle ? vehicle.patente + ' · ' + vehicleName(vehicle) : 'Vehículo no disponible') + '</h2><p><button type="button" class="text-action" data-action="open-client" data-id="' + escapeHtml(order.clienteId) + '">' + escapeHtml(clientName(client)) + '</button> · <button type="button" class="text-action" data-action="open-vehicle" data-id="' + escapeHtml(order.vehiculoId) + '">Ver ficha del vehículo</button></p></div><div class="detail-actions"><div class="order-status-control"><label for="orderStatusSelect">Estado</label><select id="orderStatusSelect" data-order-id="' + escapeHtml(id) + '">' + statusOptions(order.estado) + '</select></div><button type="button" class="button secondary" data-action="edit-order" data-id="' + escapeHtml(id) + '">Editar datos</button></div></article>' +
            '<div class="order-context">' + detailField('Kilometraje de ingreso', formatKm(order.kilometraje)) + detailField('Actualizada', formatDate(order.updatedAt)) + detailField('Problema reportado', order.problemaReportado, true) + detailField('Diagnóstico', order.diagnostico, true) + detailField('Notas', order.notas, true) + '</div>' +
            '<section class="budget-panel"><div class="budget-header"><div><span class="eyebrow">PRESUPUESTO DE LA ORDEN</span><h3>Servicios, mano de obra y repuestos</h3><p>Los repuestos se guardan como instantáneas de catálogo; no existe ni se aplica movimiento de stock.</p></div><button type="button" class="button primary" data-action="open-part-picker" data-order-id="' + escapeHtml(id) + '">+ Agregar repuesto</button></div>' +
            '<div class="line-section"><div class="line-section-header"><h4>Servicios</h4><button type="button" class="button secondary" data-action="new-line" data-order-id="' + escapeHtml(id) + '" data-kind="servicios">+ Añadir servicio</button></div><div class="line-list">' + lineRows(order, 'servicios') + '</div></div>' +
            '<div class="line-section"><div class="line-section-header"><h4>Mano de obra</h4><button type="button" class="button secondary" data-action="new-line" data-order-id="' + escapeHtml(id) + '" data-kind="manoObra">+ Añadir mano de obra</button></div><div class="line-list">' + lineRows(order, 'manoObra') + '</div></div>' +
            '<div class="line-section"><div class="line-section-header"><h4>Repuestos</h4><button type="button" class="button primary" data-action="open-part-picker" data-order-id="' + escapeHtml(id) + '">+ Agregar repuesto</button></div><div class="line-list">' + partLineRows(order) + '</div></div>' +
            '<div class="pricing-area"><div class="pricing-controls"><label>Descuento ($)<input id="orderDiscount" data-order-id="' + escapeHtml(id) + '" type="number" min="0" step="1" value="' + escapeHtml(order.descuento || 0) + '"></label><label>Impuesto (%)<input id="orderTax" data-order-id="' + escapeHtml(id) + '" type="number" min="0" max="100" step="0.01" value="' + escapeHtml(order.impuestoPorcentaje || 0) + '"></label><p class="pricing-help">El impuesto se calcula sobre el subtotal después del descuento.</p></div><div class="totals-card" id="orderTotals">' + totalsMarkup(order.totales) + '</div></div></section>';
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
        services.filter(function (service) { return service.activo || service.id === selectedId; }).forEach(function (service) { const option = document.createElement('option'); option.value = service.id; option.textContent = service.nombre + ' · ' + formatMoney(service.precioBase) + (service.activo ? '' : ' (inactivo)'); select.appendChild(option); });
        if (selectedId) select.value = selectedId;
    }
    async function openLineForm(orderId, kind, lineId) {
        const order = await repo.getWorkOrder(orderId); if (!order) return showToast('Orden no encontrada.');
        els.lineForm.reset(); els.lineForm.elements.orderId.value = orderId; els.lineForm.elements.kind.value = kind;
        els.lineForm.elements.id.value = ''; els.lineForm.elements.cantidad.value = '1'; els.lineFormError.textContent = '';
        const isService = kind === 'servicios'; document.getElementById('servicePickerLabel').hidden = !isService;
        document.getElementById('lineDialogTitle').textContent = (lineId ? 'Editar ' : 'Añadir ') + (isService ? 'servicio' : 'mano de obra');
        const line = lineId ? (order[kind] || []).find(function (item) { return item.id === lineId; }) : null;
        await populateLineServices(line && line.servicioId);
        if (line) ['id', 'servicioId', 'descripcion', 'cantidad', 'precioUnitario'].forEach(function (key) { els.lineForm.elements[key].value = line[key] == null ? '' : line[key]; });
        openDialog(els.lineDialog); setTimeout(function () { (isService ? els.lineForm.elements.servicioId : els.lineForm.elements.descripcion).focus(); }, 0);
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
        if (state.partPicker.mode === 'broad' && query.length < 2) {
            els.catalogResultMeta.textContent = 'Escribe al menos 2 caracteres para buscar en todo el catálogo.';
            els.catalogResults.innerHTML = '<div class="catalog-empty">La búsqueda amplia no confirma compatibilidad. Busca por componente, referencia OEM o código.</div>';
            return;
        }
        els.catalogResultMeta.textContent = 'Buscando…';
        try {
            const result = await CatalogAdapter.searchParts(query, {
                vehicle: state.partPicker.vehicle,
                mode: state.partPicker.mode,
                limit: 100
            });
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
        try { const saved = data.id ? await repo.updateService(data.id, data) : await repo.createService(data); els.serviceDialog.close(); await refreshSummary(); await renderList(); showToast(data.id ? 'Servicio actualizado.' : 'Servicio creado.'); await showServiceDetail(saved.id); } catch (error) { showError(els.serviceFormError, error); }
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
        if (action === 'open-order') return showOrderDetail(id); if (action === 'back-to-list') return setSection(state.section);
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
    [els.clientDialog, els.vehicleDialog, els.serviceDialog, els.orderDialog, els.lineDialog, els.partPickerDialog, els.partLineDialog].forEach(function (dialog) { dialog.addEventListener('click', function (event) { if (event.target === dialog) dialog.close(); }); });
    Object.keys(tabs).forEach(function (section) { tabs[section].addEventListener('click', function () { setSection(section); }); });
    els.addRecordButton.addEventListener('click', function () { if (state.section === 'clients') openClientForm(); if (state.section === 'vehicles') openVehicleForm(); if (state.section === 'orders') openOrderForm(); if (state.section === 'services') openServiceForm(); });
    els.recordSearch.addEventListener('input', function () { state.query = els.recordSearch.value.trim(); renderList(); });
    els.vehicleForm.elements.marca.addEventListener('input', updateModelSuggestions); els.vehicleForm.elements.modelo.addEventListener('input', updateYearSuggestions);
    els.orderForm.elements.clienteId.addEventListener('change', function () { populateOrderVehicles(els.orderForm.elements.clienteId.value); });
    els.lineForm.elements.servicioId.addEventListener('change', async function () { const service = await repo.getService(els.lineForm.elements.servicioId.value); if (!service) return; els.lineForm.elements.descripcion.value = service.nombre; els.lineForm.elements.precioUnitario.value = service.precioBase; });
    els.clientForm.addEventListener('submit', saveClient); els.vehicleForm.addEventListener('submit', saveVehicle); els.serviceForm.addEventListener('submit', saveService); els.orderForm.addEventListener('submit', saveOrder); els.lineForm.addEventListener('submit', saveLine); els.partLineForm.addEventListener('submit', savePartLine);
    els.catalogPartSearch.addEventListener('input', function () {
        clearTimeout(state.catalogSearchTimer);
        state.catalogSearchTimer = setTimeout(runCatalogPartSearch, 180);
    });
    els.plateSearch.addEventListener('input', function () { els.plateSearch.value = els.plateSearch.value.toUpperCase(); els.plateSearchMessage.textContent = ''; });
    els.plateSearchForm.addEventListener('submit', async function (event) { event.preventDefault(); const plate = TallerData.normalizePlate(els.plateSearch.value); if (!plate) { els.plateSearchMessage.textContent = 'Escribe una patente para buscar.'; return; } const vehicle = await repo.findVehicleByPlate(plate); if (!vehicle) { els.plateSearchMessage.textContent = 'No hay un vehículo registrado con esa patente.'; return; } els.plateSearchMessage.textContent = ''; await showVehicleDetail(vehicle.id); });

    Promise.all([loadCatalogNavigation(), refreshSummary()]).then(function () { return renderList(); }).catch(function (error) { els.recordList.innerHTML = '<div class="empty-state"><strong>No pudimos abrir los datos del taller</strong><p>' + escapeHtml(error.message) + '</p></div>'; });
})();
