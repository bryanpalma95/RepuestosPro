(function (global) {
    'use strict';

    const STORAGE_KEY = 'repuestospro.taller';
    const CURRENT_VERSION = 3;
    const WORK_ORDER_STATUSES = [
        'Presupuesto', 'Pendiente', 'Aprobada', 'En reparación',
        'Esperando repuesto', 'Terminada', 'Entregada', 'Cancelada'
    ];

    const CLIENT_FIELDS = [
        'nombre', 'apellido', 'rut', 'telefono', 'whatsapp', 'email',
        'direccion', 'notas'
    ];
    const VEHICLE_FIELDS = [
        'patente', 'vin', 'marca', 'modelo', 'anio', 'motor', 'cilindrada',
        'combustible', 'transmision', 'kilometraje', 'color', 'notas', 'clienteId'
    ];
    const SERVICE_FIELDS = ['nombre', 'descripcion', 'precioBase', 'duracionEstimada', 'activo'];
    const ORDER_TEXT_FIELDS = ['fecha', 'problemaReportado', 'diagnostico', 'notas', 'estado', 'clienteId', 'vehiculoId'];

    function cleanText(value, maxLength) {
        return String(value == null ? '' : value)
            .replace(/[\u0000-\u001F\u007F]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim()
            .slice(0, maxLength || 500);
    }

    function cleanNotes(value) {
        return String(value == null ? '' : value)
            .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, '')
            .trim()
            .slice(0, 3000);
    }

    function normalizeRut(value) {
        const raw = cleanText(value, 20).toUpperCase().replace(/[^0-9K]/g, '');
        if (raw.length < 2) return raw;
        return raw.slice(0, -1) + '-' + raw.slice(-1);
    }

    function normalizePlate(value) {
        return cleanText(value, 12).toUpperCase().replace(/[^A-Z0-9]/g, '');
    }

    function normalizeVin(value) {
        return cleanText(value, 17).toUpperCase().replace(/[^A-Z0-9]/g, '');
    }

    function searchText(value) {
        return cleanText(value, 500)
            .toLocaleLowerCase('es')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '');
    }

    function makeId(prefix) {
        const uuid = global.crypto && typeof global.crypto.randomUUID === 'function'
            ? global.crypto.randomUUID()
            : Date.now().toString(36) + Math.random().toString(36).slice(2);
        return prefix + '_' + uuid;
    }

    function clone(value) {
        return JSON.parse(JSON.stringify(value));
    }

    function defaultState() {
        return { version: CURRENT_VERSION, clients: [], vehicles: [], services: [], workOrders: [] };
    }

    function toNonNegativeNumber(value, fallback) {
        const number = Number(value);
        return Number.isFinite(number) && number >= 0 ? number : (fallback == null ? 0 : fallback);
    }

    function roundMoney(value) {
        return Math.round((Number(value) + Number.EPSILON) * 100) / 100;
    }

    function sanitizeClient(input) {
        const output = {};
        CLIENT_FIELDS.forEach(function (field) {
            output[field] = field === 'notas'
                ? cleanNotes(input[field])
                : cleanText(input[field], field === 'direccion' ? 300 : 160);
        });
        output.rut = normalizeRut(output.rut);
        output.email = output.email.toLowerCase();
        return output;
    }

    function sanitizeVehicle(input) {
        const output = {};
        VEHICLE_FIELDS.forEach(function (field) {
            output[field] = field === 'notas'
                ? cleanNotes(input[field])
                : cleanText(input[field], 160);
        });
        output.patente = normalizePlate(output.patente);
        output.vin = normalizeVin(output.vin);
        output.anio = output.anio ? Number.parseInt(output.anio, 10) : null;
        output.kilometraje = output.kilometraje === '' ? null : Number.parseInt(output.kilometraje, 10);
        return output;
    }

    function sanitizeService(input) {
        const output = {};
        SERVICE_FIELDS.forEach(function (field) {
            output[field] = cleanText(input[field], field === 'descripcion' ? 1000 : 160);
        });
        output.precioBase = roundMoney(toNonNegativeNumber(input.precioBase));
        output.duracionEstimada = input.duracionEstimada === '' || input.duracionEstimada == null
            ? null
            : Math.round(toNonNegativeNumber(input.duracionEstimada));
        output.activo = input.activo === true || input.activo === 'true' || input.activo === 'on' || input.activo === '1';
        return output;
    }

    function sanitizeLine(input, prefix) {
        const quantity = Math.max(0.01, toNonNegativeNumber(input.cantidad, 1));
        const unitPrice = roundMoney(toNonNegativeNumber(input.precioUnitario));
        return {
            id: cleanText(input.id, 100) || makeId(prefix),
            servicioId: prefix === 'srvline' ? cleanText(input.servicioId, 100) : '',
            descripcion: cleanText(input.descripcion, 500),
            cantidad: quantity,
            precioUnitario: unitPrice,
            subtotal: roundMoney(quantity * unitPrice)
        };
    }

    function sanitizeCatalogSnapshot(input) {
        const snapshot = input && typeof input === 'object' ? input : {};
        return {
            catalogId: cleanText(snapshot.catalogId || snapshot.id, 300),
            vehicleKey: cleanText(snapshot.vehicleKey, 300),
            vehicleName: cleanText(snapshot.vehicleName, 300),
            vehicleInfo: cleanText(snapshot.vehicleInfo, 500),
            category: cleanText(snapshot.category, 160),
            name: cleanText(snapshot.name, 300),
            details: cleanText(snapshot.details, 1500),
            brands: (Array.isArray(snapshot.brands) ? snapshot.brands : []).map(function (brand) { return cleanText(brand, 160); }).filter(Boolean).slice(0, 30),
            references: (Array.isArray(snapshot.references) ? snapshot.references : []).map(function (reference) {
                return { code: cleanText(reference.code, 160), status: cleanText(reference.status, 40) };
            }).filter(function (reference) { return reference.code; }).slice(0, 50),
            links: (Array.isArray(snapshot.links) ? snapshot.links : []).map(function (link) {
                const url = cleanText(link.url, 1000);
                if (!/^https?:\/\//i.test(url)) return null;
                return { label: cleanText(link.label, 120) || 'Fuente', url: url };
            }).filter(Boolean).slice(0, 20),
            interval: cleanText(snapshot.interval, 120),
            compatibility: (Array.isArray(snapshot.compatibility) ? snapshot.compatibility : []).map(function (item) {
                return { marca: cleanText(item.marca, 160), modelos: cleanText(item.modelos, 1000) };
            }).filter(function (item) { return item.marca || item.modelos; }).slice(0, 100),
            matchMode: snapshot.matchMode === 'compatible' ? 'compatible' : 'broad',
            compatibilityConfirmed: snapshot.compatibilityConfirmed === true,
            catalogVehicleMatch: cleanText(snapshot.catalogVehicleMatch, 300),
            capturedAt: cleanText(snapshot.capturedAt, 80) || new Date().toISOString()
        };
    }

    function sanitizePartLine(input) {
        const quantity = Math.max(0.01, toNonNegativeNumber(input.cantidad, 1));
        const hasPrice = input.precioUnitario !== '' && input.precioUnitario != null;
        const unitPrice = hasPrice ? roundMoney(toNonNegativeNumber(input.precioUnitario)) : null;
        return {
            id: cleanText(input.id, 100) || makeId('partline'),
            cantidad: quantity,
            precioUnitario: unitPrice,
            subtotal: unitPrice == null ? 0 : roundMoney(quantity * unitPrice),
            catalogSnapshot: sanitizeCatalogSnapshot(input.catalogSnapshot)
        };
    }

    function calculateTotals(order) {
        const serviciosSubtotal = roundMoney((order.servicios || []).reduce(function (sum, line) { return sum + toNonNegativeNumber(line.subtotal); }, 0));
        const manoObraSubtotal = roundMoney((order.manoObra || []).reduce(function (sum, line) { return sum + toNonNegativeNumber(line.subtotal); }, 0));
        const repuestosSubtotal = roundMoney((order.repuestos || []).reduce(function (sum, line) { return sum + toNonNegativeNumber(line.subtotal); }, 0));
        const subtotal = roundMoney(serviciosSubtotal + manoObraSubtotal + repuestosSubtotal);
        const requestedDiscount = roundMoney(toNonNegativeNumber(order.descuento));
        const descuento = Math.min(requestedDiscount, subtotal);
        const baseImponible = roundMoney(subtotal - descuento);
        const impuestoPorcentaje = Math.min(100, toNonNegativeNumber(order.impuestoPorcentaje));
        const impuesto = roundMoney(baseImponible * impuestoPorcentaje / 100);
        return {
            serviciosSubtotal: serviciosSubtotal,
            manoObraSubtotal: manoObraSubtotal,
            repuestosSubtotal: repuestosSubtotal,
            subtotal: subtotal,
            descuento: descuento,
            baseImponible: baseImponible,
            impuestoPorcentaje: impuestoPorcentaje,
            impuesto: impuesto,
            total: roundMoney(baseImponible + impuesto)
        };
    }

    function sanitizeOrder(input) {
        const output = {};
        ORDER_TEXT_FIELDS.forEach(function (field) {
            output[field] = field === 'notas' || field === 'diagnostico' || field === 'problemaReportado'
                ? cleanNotes(input[field])
                : cleanText(input[field], 160);
        });
        output.estado = WORK_ORDER_STATUSES.includes(output.estado) ? output.estado : WORK_ORDER_STATUSES[0];
        output.closedAt = cleanText(input.closedAt, 40);
        output.kilometraje = input.kilometraje === '' || input.kilometraje == null
            ? null
            : Math.round(toNonNegativeNumber(input.kilometraje));
        output.servicios = Array.isArray(input.servicios)
            ? input.servicios.map(function (line) { return sanitizeLine(line, 'srvline'); })
            : [];
        output.manoObra = Array.isArray(input.manoObra)
            ? input.manoObra.map(function (line) { return sanitizeLine(line, 'labline'); })
            : [];
        output.repuestos = Array.isArray(input.repuestos)
            ? input.repuestos.map(function (line) { return sanitizePartLine(line); })
            : [];
        output.descuento = roundMoney(toNonNegativeNumber(input.descuento));
        output.impuestoPorcentaje = Math.min(100, toNonNegativeNumber(input.impuestoPorcentaje));
        output.totales = calculateTotals(output);
        return output;
    }

    function nextOrderIdentifier(state) {
        const year = new Date().getFullYear();
        const prefix = 'OT-' + year + '-';
        const maximum = (state.workOrders || []).reduce(function (max, order) {
            if (!String(order.identificador || '').startsWith(prefix)) return max;
            const number = Number.parseInt(String(order.identificador).slice(prefix.length), 10);
            return Number.isFinite(number) ? Math.max(max, number) : max;
        }, 0);
        return prefix + String(maximum + 1).padStart(4, '0');
    }

    function migrate(parsed) {
        if (!parsed || typeof parsed !== 'object') return defaultState();
        const state = {
            version: Number(parsed.version) || 1,
            clients: Array.isArray(parsed.clients) ? parsed.clients : [],
            vehicles: Array.isArray(parsed.vehicles) ? parsed.vehicles : [],
            services: Array.isArray(parsed.services) ? parsed.services : [],
            workOrders: Array.isArray(parsed.workOrders) ? parsed.workOrders.map(function (order) {
                return Object.assign({ repuestos: [] }, order);
            }) : []
        };

        // Migraciones aditivas: v1 añadió operación; v3 agrega repuestos dentro de cada orden.
        state.version = CURRENT_VERSION;
        return state;
    }

    class LocalWorkshopRepository {
        constructor(storage) {
            this.storage = storage || global.localStorage;
        }

        _read() {
            try {
                const raw = this.storage.getItem(STORAGE_KEY);
                return raw ? migrate(JSON.parse(raw)) : defaultState();
            } catch (error) {
                throw new Error('No fue posible leer los datos locales del taller.');
            }
        }

        _write(state) {
            try {
                state.version = CURRENT_VERSION;
                this.storage.setItem(STORAGE_KEY, JSON.stringify(state));
                return clone(state);
            } catch (error) {
                throw new Error('No fue posible guardar. Revisa el espacio disponible del navegador.');
            }
        }

        async getSummary() {
            const state = this._read();
            return {
                clients: state.clients.length,
                vehicles: state.vehicles.length,
                workOrders: state.workOrders.length,
                activeServices: state.services.filter(function (service) { return service.activo; }).length
            };
        }

        async listClients(query) {
            const q = searchText(query);
            return clone(this._read().clients)
                .filter(function (client) {
                    if (!q) return true;
                    return searchText([client.nombre, client.apellido, client.rut, client.telefono, client.whatsapp, client.email].join(' ')).includes(q);
                })
                .sort(function (a, b) {
                    return (a.apellido + ' ' + a.nombre).localeCompare(b.apellido + ' ' + b.nombre, 'es');
                });
        }

        async getClient(id) {
            const client = this._read().clients.find(function (item) { return item.id === id; });
            return client ? clone(client) : null;
        }

        async createClient(input) {
            const state = this._read();
            const data = sanitizeClient(input || {});
            const now = new Date().toISOString();
            const record = Object.assign({ id: makeId('cli'), createdAt: now, updatedAt: now }, data);
            state.clients.push(record);
            this._write(state);
            return clone(record);
        }

        async updateClient(id, input) {
            const state = this._read();
            const index = state.clients.findIndex(function (item) { return item.id === id; });
            if (index < 0) throw new Error('Cliente no encontrado.');
            state.clients[index] = Object.assign({}, state.clients[index], sanitizeClient(input || {}), {
                id: state.clients[index].id,
                createdAt: state.clients[index].createdAt,
                updatedAt: new Date().toISOString()
            });
            this._write(state);
            return clone(state.clients[index]);
        }

        async deleteClient(id) {
            const state = this._read();
            const hasVehicles = state.vehicles.some(function (vehicle) { return vehicle.clienteId === id; });
            const hasOrders = state.workOrders.some(function (order) { return order.clienteId === id; });
            if (hasVehicles || hasOrders) throw new Error('Elimina o reasigna los vehículos y órdenes asociados antes de borrar este cliente.');
            const before = state.clients.length;
            state.clients = state.clients.filter(function (item) { return item.id !== id; });
            if (state.clients.length === before) throw new Error('Cliente no encontrado.');
            this._write(state);
            return true;
        }

        async listVehicles(query, clientId) {
            const q = searchText(query);
            const state = this._read();
            return clone(state.vehicles)
                .filter(function (vehicle) {
                    if (clientId && vehicle.clienteId !== clientId) return false;
                    if (!q) return true;
                    const client = state.clients.find(function (item) { return item.id === vehicle.clienteId; });
                    return searchText([vehicle.patente, vehicle.vin, vehicle.marca, vehicle.modelo, vehicle.anio,
                        client ? client.nombre : '', client ? client.apellido : '']
                        .join(' ')).includes(q);
                })
                .sort(function (a, b) { return a.patente.localeCompare(b.patente, 'es'); });
        }

        async getVehicle(id) {
            const vehicle = this._read().vehicles.find(function (item) { return item.id === id; });
            return vehicle ? clone(vehicle) : null;
        }

        async findVehicleByPlate(plate) {
            const normalized = normalizePlate(plate);
            if (!normalized) return null;
            const vehicle = this._read().vehicles.find(function (item) { return item.patente === normalized; });
            return vehicle ? clone(vehicle) : null;
        }

        async createVehicle(input) {
            const state = this._read();
            const data = sanitizeVehicle(input || {});
            const now = new Date().toISOString();
            const record = Object.assign({ id: makeId('veh'), createdAt: now, updatedAt: now }, data);
            state.vehicles.push(record);
            this._write(state);
            return clone(record);
        }

        async updateVehicle(id, input) {
            const state = this._read();
            const index = state.vehicles.findIndex(function (item) { return item.id === id; });
            if (index < 0) throw new Error('Vehículo no encontrado.');
            state.vehicles[index] = Object.assign({}, state.vehicles[index], sanitizeVehicle(input || {}), {
                id: state.vehicles[index].id,
                createdAt: state.vehicles[index].createdAt,
                updatedAt: new Date().toISOString()
            });
            this._write(state);
            return clone(state.vehicles[index]);
        }

        async deleteVehicle(id) {
            const state = this._read();
            if (state.workOrders.some(function (order) { return order.vehiculoId === id; })) {
                throw new Error('Este vehículo tiene órdenes en su historial y no puede eliminarse.');
            }
            const before = state.vehicles.length;
            state.vehicles = state.vehicles.filter(function (item) { return item.id !== id; });
            if (state.vehicles.length === before) throw new Error('Vehículo no encontrado.');
            this._write(state);
            return true;
        }

        async listServices(query, includeInactive) {
            const q = searchText(query);
            return clone(this._read().services)
                .filter(function (service) {
                    if (!includeInactive && !service.activo) return false;
                    return !q || searchText(service.nombre + ' ' + service.descripcion).includes(q);
                })
                .sort(function (a, b) { return a.nombre.localeCompare(b.nombre, 'es'); });
        }

        async getService(id) {
            const service = this._read().services.find(function (item) { return item.id === id; });
            return service ? clone(service) : null;
        }

        async createService(input) {
            const state = this._read();
            const data = sanitizeService(input || {});
            const now = new Date().toISOString();
            const record = Object.assign({ id: makeId('srv'), createdAt: now, updatedAt: now }, data);
            state.services.push(record);
            this._write(state);
            return clone(record);
        }

        async updateService(id, input) {
            const state = this._read();
            const index = state.services.findIndex(function (item) { return item.id === id; });
            if (index < 0) throw new Error('Servicio no encontrado.');
            state.services[index] = Object.assign({}, state.services[index], sanitizeService(input || {}), {
                id: state.services[index].id,
                createdAt: state.services[index].createdAt,
                updatedAt: new Date().toISOString()
            });
            this._write(state);
            return clone(state.services[index]);
        }

        async deleteService(id) {
            const state = this._read();
            const before = state.services.length;
            state.services = state.services.filter(function (item) { return item.id !== id; });
            if (state.services.length === before) throw new Error('Servicio no encontrado.');
            this._write(state);
            return true;
        }

        async listWorkOrders(query, vehicleId) {
            const q = searchText(query);
            const state = this._read();
            return clone(state.workOrders)
                .filter(function (order) {
                    if (vehicleId && order.vehiculoId !== vehicleId) return false;
                    if (!q) return true;
                    const client = state.clients.find(function (item) { return item.id === order.clienteId; });
                    const vehicle = state.vehicles.find(function (item) { return item.id === order.vehiculoId; });
                    return searchText([
                        order.identificador, order.estado, order.fecha, order.problemaReportado,
                        client ? client.nombre : '', client ? client.apellido : '',
                        vehicle ? vehicle.patente : '', vehicle ? vehicle.marca : '', vehicle ? vehicle.modelo : ''
                    ].join(' ')).includes(q);
                })
                .sort(function (a, b) {
                    return String(b.fecha).localeCompare(String(a.fecha)) || String(b.createdAt).localeCompare(String(a.createdAt));
                });
        }

        async getWorkOrder(id) {
            const order = this._read().workOrders.find(function (item) { return item.id === id; });
            return order ? clone(order) : null;
        }

        _assertOrderLinks(state, data) {
            const client = state.clients.find(function (item) { return item.id === data.clienteId; });
            const vehicle = state.vehicles.find(function (item) { return item.id === data.vehiculoId; });
            if (!client || !vehicle) throw new Error('La orden debe vincular un cliente y vehículo existentes.');
            if (vehicle.clienteId !== client.id) throw new Error('El vehículo seleccionado no pertenece a ese cliente.');
        }

        async createWorkOrder(input) {
            const state = this._read();
            const data = sanitizeOrder(input || {});
            this._assertOrderLinks(state, data);
            const now = new Date().toISOString();
            const record = Object.assign({
                id: makeId('ord'),
                identificador: nextOrderIdentifier(state),
                createdAt: now,
                updatedAt: now
            }, data);
            state.workOrders.push(record);
            this._write(state);
            return clone(record);
        }

        async updateWorkOrder(id, input) {
            const state = this._read();
            const index = state.workOrders.findIndex(function (item) { return item.id === id; });
            if (index < 0) throw new Error('Orden de trabajo no encontrada.');
            const merged = Object.assign({}, state.workOrders[index], input || {});
            const data = sanitizeOrder(merged);
            this._assertOrderLinks(state, data);
            state.workOrders[index] = Object.assign({}, state.workOrders[index], data, {
                id: state.workOrders[index].id,
                identificador: state.workOrders[index].identificador,
                createdAt: state.workOrders[index].createdAt,
                updatedAt: new Date().toISOString()
            });
            this._write(state);
            return clone(state.workOrders[index]);
        }

        async setWorkOrderStatus(id, status) {
            if (!WORK_ORDER_STATUSES.includes(status)) throw new Error('Estado de orden no válido.');
            const isClosed = status === 'Entregada' || status === 'Cancelada';
            const current = await this.getWorkOrder(id);
            return this.updateWorkOrder(id, {
                estado: status,
                closedAt: isClosed ? (current && current.closedAt ? current.closedAt : new Date().toISOString()) : ''
            });
        }

        async closeWorkOrder(id) {
            return this.updateWorkOrder(id, { estado: 'Entregada', closedAt: new Date().toISOString() });
        }

        async reopenWorkOrder(id) {
            return this.updateWorkOrder(id, { estado: 'En reparación', closedAt: '' });
        }

        async saveOrderLine(orderId, kind, input) {
            if (kind !== 'servicios' && kind !== 'manoObra' && kind !== 'repuestos') throw new Error('Tipo de línea no válido.');
            const state = this._read();
            const index = state.workOrders.findIndex(function (item) { return item.id === orderId; });
            if (index < 0) throw new Error('Orden de trabajo no encontrada.');
            if (state.workOrders[index].estado === 'Entregada' || state.workOrders[index].estado === 'Cancelada') throw new Error('La orden está cerrada. Reábrela antes de modificar sus líneas.');
            const lines = Array.isArray(state.workOrders[index][kind]) ? state.workOrders[index][kind].slice() : [];
            const requestedId = cleanText(input && input.id, 100);
            const lineIndex = lines.findIndex(function (item) { return item.id === requestedId; });
            const source = lineIndex < 0 ? (input || {}) : Object.assign({}, lines[lineIndex], input || {});
            if (lineIndex >= 0 && kind === 'repuestos' && !(input && input.catalogSnapshot)) source.catalogSnapshot = lines[lineIndex].catalogSnapshot;
            const line = kind === 'repuestos'
                ? sanitizePartLine(source)
                : sanitizeLine(source, kind === 'servicios' ? 'srvline' : 'labline');
            if (lineIndex < 0) lines.push(line); else lines[lineIndex] = line;
            state.workOrders[index][kind] = lines;
            const refreshed = sanitizeOrder(state.workOrders[index]);
            state.workOrders[index] = Object.assign({}, state.workOrders[index], refreshed, { updatedAt: new Date().toISOString() });
            this._write(state);
            return clone(state.workOrders[index]);
        }

        async deleteOrderLine(orderId, kind, lineId) {
            if (kind !== 'servicios' && kind !== 'manoObra' && kind !== 'repuestos') throw new Error('Tipo de línea no válido.');
            const state = this._read();
            const index = state.workOrders.findIndex(function (item) { return item.id === orderId; });
            if (index < 0) throw new Error('Orden de trabajo no encontrada.');
            if (state.workOrders[index].estado === 'Entregada' || state.workOrders[index].estado === 'Cancelada') throw new Error('La orden está cerrada. Reábrela antes de modificar sus líneas.');
            state.workOrders[index][kind] = (state.workOrders[index][kind] || []).filter(function (line) { return line.id !== lineId; });
            const refreshed = sanitizeOrder(state.workOrders[index]);
            state.workOrders[index] = Object.assign({}, state.workOrders[index], refreshed, { updatedAt: new Date().toISOString() });
            this._write(state);
            return clone(state.workOrders[index]);
        }

        async updateOrderPricing(id, discount, taxPercent) {
            const current = await this.getWorkOrder(id);
            if (!current) throw new Error('Orden de trabajo no encontrada.');
            if (current.estado === 'Entregada' || current.estado === 'Cancelada') throw new Error('La orden está cerrada. Reábrela antes de modificar sus totales.');
            return this.updateWorkOrder(id, { descuento: discount, impuestoPorcentaje: taxPercent });
        }

        async isRutAvailable(rut, exceptId) {
            const normalized = normalizeRut(rut);
            if (!normalized) return true;
            return !this._read().clients.some(function (item) {
                return item.id !== exceptId && normalizeRut(item.rut) === normalized;
            });
        }

        async isPlateAvailable(plate, exceptId) {
            const normalized = normalizePlate(plate);
            return !this._read().vehicles.some(function (item) {
                return item.id !== exceptId && item.patente === normalized;
            });
        }

        async isVinAvailable(vin, exceptId) {
            const normalized = normalizeVin(vin);
            if (!normalized) return true;
            return !this._read().vehicles.some(function (item) {
                return item.id !== exceptId && item.vin === normalized;
            });
        }
    }

    global.TallerData = Object.freeze({
        CURRENT_VERSION: CURRENT_VERSION,
        STORAGE_KEY: STORAGE_KEY,
        WORK_ORDER_STATUSES: WORK_ORDER_STATUSES.slice(),
        LocalWorkshopRepository: LocalWorkshopRepository,
        normalizePlate: normalizePlate,
        normalizeRut: normalizeRut,
        normalizeVin: normalizeVin
    });
})(window);
