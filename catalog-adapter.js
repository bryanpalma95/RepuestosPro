(function (global) {
    'use strict';

    function cleanText(value, maxLength) {
        return String(value == null ? '' : value)
            .replace(/[\u0000-\u001F\u007F]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim()
            .slice(0, maxLength || 1000);
    }

    function normalizeText(value) {
        return cleanText(value, 2000)
            .toLocaleLowerCase('es')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[^a-z0-9]+/g, ' ')
            .trim();
    }

    function slug(value) {
        return normalizeText(value).replace(/\s+/g, '-');
    }

    function compact(value) {
        return normalizeText(value).replace(/[^a-z0-9]/g, '');
    }

    function compatibilityKey(value) {
        return String(value || '').toUpperCase().replace(/\s+/g, '');
    }

    function isPlaceholderReference(value) {
        const reference = normalizeText(value);
        return !reference
            || reference.startsWith('verificar ')
            || reference.includes(' por modelo')
            || reference.includes(' por motor')
            || reference.includes(' segun ')
            || reference === 'segun vin';
    }

    function referencePriority(reference) {
        return (isPlaceholderReference(reference.code) ? 20 : 0)
            + (reference.status === 'confirmed' ? 0 : 1);
    }

    function safeLinks(links) {
        if (!Array.isArray(links)) return [];
        return links.map(function (link) {
            const url = cleanText(link && link.u, 1000);
            if (!/^https?:\/\//i.test(url)) return null;
            return { label: cleanText(link.t, 120) || 'Fuente', url: url };
        }).filter(Boolean);
    }

    function uniqueCompatibility(items) {
        const seen = new Set();
        return items.filter(function (item) {
            const key = item.marca + '|' + item.modelos;
            if (seen.has(key)) return false;
            seen.add(key);
            return true;
        });
    }

    class ReadOnlyCatalogAdapter {
        constructor(options) {
            const settings = options || {};
            this.dbUrl = settings.dbUrl || 'db.json';
            this.compatUrl = settings.compatUrl || 'db-compat.json';
            this.fetcher = settings.fetcher || global.fetch.bind(global);
            this.loaded = false;
            this.loading = null;
            this.database = {};
            this.compatibility = {};
            this.parts = [];
            this.partsByVehicle = new Map();
        }

        async _fetchJson(url) {
            const response = await this.fetcher(url);
            if (!response || !response.ok) throw new Error('No fue posible leer ' + url + '.');
            return response.json();
        }

        async load() {
            if (this.loaded) return this;
            if (this.loading) return this.loading;
            this.loading = Promise.all([this._fetchJson(this.dbUrl), this._fetchJson(this.compatUrl)])
                .then(function (payload) {
                    this.database = payload[0] && typeof payload[0] === 'object' ? payload[0] : {};
                    this.compatibility = payload[1] && typeof payload[1] === 'object' ? payload[1] : {};
                    this._buildIndex();
                    this.loaded = true;
                    return this;
                }.bind(this))
                .catch(function (error) {
                    this.loading = null;
                    throw error;
                }.bind(this));
            return this.loading;
        }

        _buildIndex() {
            this.parts = [];
            this.partsByVehicle = new Map();
            Object.entries(this.database).forEach(function (vehicleEntry) {
                const vehicleKey = vehicleEntry[0];
                const vehicle = vehicleEntry[1] || {};
                const vehicleParts = [];
                Object.entries(vehicle.categories || {}).forEach(function (categoryEntry, categoryIndex) {
                    const groupName = categoryEntry[0];
                    (categoryEntry[1] || []).forEach(function (rawPart, partIndex) {
                        const references = (rawPart.refs || []).map(function (reference) {
                            return { code: cleanText(reference.r, 160), status: cleanText(reference.s, 40) };
                        }).filter(function (reference) { return reference.code; }).sort(function (a, b) {
                            return referencePriority(a) - referencePriority(b);
                        });
                        const compatibilities = [];
                        references.forEach(function (reference) {
                            const entry = this.compatibility[compatibilityKey(reference.code)];
                            if (!entry) return;
                            (entry.compatibles || []).forEach(function (item) {
                                compatibilities.push({
                                    marca: cleanText(item.marca, 160),
                                    modelos: cleanText(item.modelos, 1000)
                                });
                            });
                        }.bind(this));
                        const category = cleanText(rawPart.cat || groupName, 160);
                        const name = cleanText(rawPart.name || rawPart.cat || groupName, 300);
                        const details = cleanText(rawPart.details, 1500);
                        const brands = cleanText(rawPart.brands, 500).split(/[,;]+/).map(function (brand) { return brand.trim(); }).filter(Boolean);
                        const part = {
                            id: vehicleKey + ':' + categoryIndex + ':' + partIndex,
                            vehicleKey: vehicleKey,
                            vehicleName: cleanText(vehicle.name, 300),
                            vehicleInfo: cleanText(vehicle.info, 500),
                            category: category,
                            name: name,
                            details: details,
                            brands: brands,
                            references: references,
                            links: safeLinks(rawPart.links),
                            interval: cleanText(rawPart.interval, 120),
                            compatibility: uniqueCompatibility(compatibilities),
                            price: null
                        };
                        part._search = normalizeText([
                            part.category, part.name, part.details, part.brands.join(' '),
                            part.references.map(function (reference) { return reference.code; }).join(' '),
                            part.vehicleName, part.vehicleInfo
                        ].join(' '));
                        part._compact = compact(part._search);
                        this.parts.push(part);
                        vehicleParts.push(part);
                    }.bind(this));
                }.bind(this));
                this.partsByVehicle.set(vehicleKey, vehicleParts);
            }.bind(this));
        }

        async matchVehicle(vehicle) {
            await this.load();
            const marca = cleanText(vehicle && vehicle.marca, 100);
            const modelo = cleanText(vehicle && vehicle.modelo, 160);
            const anio = String(vehicle && vehicle.anio || '').trim();
            const motor = cleanText(vehicle && vehicle.motor, 160);
            if (!marca || !modelo || !/^\d{4}$/.test(anio)) {
                return { confirmed: false, reason: 'Datos insuficientes: se requieren marca, modelo y año.' };
            }
            const expected = slug(marca) + '-' + slug(modelo) + '-' + anio;
            let vehicleKey = Object.prototype.hasOwnProperty.call(this.database, expected) ? expected : '';
            if (!vehicleKey) {
                const brandPrefix = slug(marca) + '-';
                const modelFragment = '-' + slug(modelo) + '-';
                vehicleKey = Object.keys(this.database).find(function (key) {
                    return key.startsWith(brandPrefix) && key.includes(modelFragment) && key.endsWith('-' + anio);
                }) || '';
            }
            if (!vehicleKey) {
                return { confirmed: false, reason: 'No hay una coincidencia exacta de marca, modelo y año en el catálogo.' };
            }
            const record = this.database[vehicleKey] || {};
            const engineMatched = motor ? normalizeText(record.info).includes(normalizeText(motor)) : null;
            return {
                confirmed: true,
                vehicleKey: vehicleKey,
                vehicleName: cleanText(record.name, 300),
                vehicleInfo: cleanText(record.info, 500),
                engineProvided: Boolean(motor),
                engineMatched: engineMatched,
                reason: engineMatched === false
                    ? 'Marca, modelo y año coinciden; el motor no está confirmado en la ficha técnica.'
                    : 'Coincidencia exacta de marca, modelo y año.'
            };
        }

        _publicPart(part, mode, match) {
            return {
                id: part.id,
                vehicleKey: part.vehicleKey,
                vehicleName: part.vehicleName,
                vehicleInfo: part.vehicleInfo,
                category: part.category,
                name: part.name,
                details: part.details,
                brands: part.brands.slice(),
                references: part.references.map(function (reference) { return Object.assign({}, reference); }),
                links: part.links.map(function (link) { return Object.assign({}, link); }),
                interval: part.interval,
                compatibility: part.compatibility.map(function (item) { return Object.assign({}, item); }),
                price: null,
                matchMode: mode,
                compatibilityConfirmed: mode === 'compatible' && Boolean(match && match.confirmed),
                catalogVehicleMatch: match && match.vehicleKey === part.vehicleKey ? match.vehicleName : ''
            };
        }

        _matchesQuery(part, query) {
            const normalized = normalizeText(query);
            if (!normalized) return true;
            const tokens = normalized.split(/\s+/).filter(Boolean);
            const normalMatch = tokens.every(function (token) { return part._search.includes(token); });
            return normalMatch || part._compact.includes(compact(query));
        }

        async findCompatibleParts(vehicle) {
            const match = await this.matchVehicle(vehicle || {});
            const source = match.confirmed ? (this.partsByVehicle.get(match.vehicleKey) || []) : [];
            return {
                mode: match.confirmed ? 'compatible' : 'broad',
                match: match,
                parts: source.map(function (part) { return this._publicPart(part, 'compatible', match); }.bind(this))
            };
        }

        async searchParts(query, options) {
            await this.load();
            const settings = options || {};
            const match = await this.matchVehicle(settings.vehicle || {});
            const requestedMode = settings.mode === 'broad' ? 'broad' : 'compatible';
            const mode = requestedMode === 'compatible' && match.confirmed ? 'compatible' : 'broad';
            const source = mode === 'compatible' ? (this.partsByVehicle.get(match.vehicleKey) || []) : this.parts;
            const limit = Math.max(1, Math.min(Number(settings.limit) || 80, 200));
            let results = source.filter(function (part) { return this._matchesQuery(part, query); }.bind(this));
            if (mode === 'broad' && match.confirmed) {
                results.sort(function (a, b) {
                    return Number(b.vehicleKey === match.vehicleKey) - Number(a.vehicleKey === match.vehicleKey);
                });
            }
            return {
                mode: mode,
                match: match,
                total: results.length,
                parts: results.slice(0, limit).map(function (part) { return this._publicPart(part, mode, match); }.bind(this))
            };
        }
    }

    const adapter = new ReadOnlyCatalogAdapter();
    global.CatalogAdapter = Object.freeze({
        ReadOnlyCatalogAdapter: ReadOnlyCatalogAdapter,
        findCompatibleParts: adapter.findCompatibleParts.bind(adapter),
        searchParts: adapter.searchParts.bind(adapter),
        matchVehicle: adapter.matchVehicle.bind(adapter),
        isLoaded: function () { return adapter.loaded; }
    });
})(window);
