--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.13
-- Dumped by pg_dump version 9.6.13

-- Started on 2019-07-06 08:41:20 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE "rHorta";
--
-- TOC entry 2161 (class 1262 OID 16385)
-- Name: rHorta; Type: DATABASE; Schema: -; Owner: pi
--

CREATE DATABASE "rHorta" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'es_ES.UTF-8' LC_CTYPE = 'es_ES.UTF-8';


ALTER DATABASE "rHorta" OWNER TO pi;

\connect "rHorta"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12393)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2164 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 186 (class 1259 OID 16391)
-- Name: eventos_rego; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.eventos_rego (
    id integer NOT NULL,
    inicio timestamp without time zone,
    fin timestamp without time zone,
    zona character varying(50)
);


ALTER TABLE public.eventos_rego OWNER TO pi;

--
-- TOC entry 185 (class 1259 OID 16386)
-- Name: propiedades; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.propiedades (
    clave character varying(50) NOT NULL,
    valor character varying(255)
);


ALTER TABLE public.propiedades OWNER TO pi;

--
-- TOC entry 187 (class 1259 OID 16410)
-- Name: sensores_mi_flora; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.sensores_mi_flora (
    mac_addr character varying(50) NOT NULL,
    humidade numeric,
    temperatura numeric,
    nombre character varying(255),
    nivel_ph numeric,
    luz_solar numeric,
    nivel_bateria numeric,
    firmware character varying(10),
    ultima_medicion timestamp without time zone,
    zona character varying
);


ALTER TABLE public.sensores_mi_flora OWNER TO pi;

--
-- TOC entry 188 (class 1259 OID 16424)
-- Name: sensores_mi_flora_historico; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.sensores_mi_flora_historico (
    mac_addr character varying(50) NOT NULL,
    humidade numeric,
    temperatura numeric,
    nombre character varying(255),
    nivel_ph numeric,
    luz_solar numeric,
    nivel_bateria numeric,
    firmware character varying(10),
    fecha timestamp without time zone NOT NULL,
    zona character varying(50)
);


ALTER TABLE public.sensores_mi_flora_historico OWNER TO pi;

--
-- TOC entry 189 (class 1259 OID 16432)
-- Name: zona; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.zona (
    id_zona character varying(50) NOT NULL,
    canal_gpio integer,
    tope_riegos integer,
    min_humidade numeric,
    max_humidade numeric
);


ALTER TABLE public.zona OWNER TO pi;

--
-- TOC entry 2152 (class 0 OID 16391)
-- Dependencies: 186
-- Data for Name: eventos_rego; Type: TABLE DATA; Schema: public; Owner: pi
--

INSERT INTO public.eventos_rego (id, inicio, fin, zona) VALUES (20, '2019-07-05 22:24:41.463947', '2019-07-05 22:24:56.547402', 'maceta_1');
INSERT INTO public.eventos_rego (id, inicio, fin, zona) VALUES (21, '2019-07-05 22:26:43.424063', '2019-07-05 22:26:58.499741', 'maceta_1');
INSERT INTO public.eventos_rego (id, inicio, fin, zona) VALUES (22, '2019-07-05 22:28:01.66', '2019-07-05 22:28:08.732918', 'maceta_1');


--
-- TOC entry 2151 (class 0 OID 16386)
-- Dependencies: 185
-- Data for Name: propiedades; Type: TABLE DATA; Schema: public; Owner: pi
--

INSERT INTO public.propiedades (clave, valor) VALUES ('id_evento', '23');
INSERT INTO public.propiedades (clave, valor) VALUES ('estado_rego', 'INACTIVO');


--
-- TOC entry 2153 (class 0 OID 16410)
-- Dependencies: 187
-- Data for Name: sensores_mi_flora; Type: TABLE DATA; Schema: public; Owner: pi
--

INSERT INTO public.sensores_mi_flora (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, ultima_medicion, zona) VALUES ('C4:7C:8D:6A:EB:DE', 0, 24.3, 'mi_flora_1', 0, 237, 100, '3.1.9', '2019-07-05 22:44:49.060792', 'maceta_1');
INSERT INTO public.sensores_mi_flora (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, ultima_medicion, zona) VALUES ('C4:7C:8D:6A:80:84', 0, 25.1, 'mi_flora_2', 0, 214, 100, '3.2.1', '2019-07-05 22:44:49.097911', 'maceta_1');


--
-- TOC entry 2154 (class 0 OID 16424)
-- Dependencies: 188
-- Data for Name: sensores_mi_flora_historico; Type: TABLE DATA; Schema: public; Owner: pi
--

INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:EB:DE', 0, 26.0, 'Flower care', 0, 148, 100, '3.1.9', '2019-07-05 22:36:14.943948', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:80:84', 0, 27.3, 'Flower care', 0, 104, 100, '3.2.1', '2019-07-05 22:36:15.015899', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:EB:DE', 0, 24.3, 'Flower care', 0, 26, 100, '3.1.9', '2019-07-05 22:38:49.113215', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:80:84', 0, 25.0, 'Flower care', 0, 0, 100, '3.2.1', '2019-07-05 22:38:49.171855', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:EB:DE', 0, 24.4, 'Flower care', 0, 178, 100, '3.1.9', '2019-07-05 22:43:02.998691', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:80:84', 0, 25.3, 'Flower care', 0, 154, 100, '3.2.1', '2019-07-05 22:43:03.039005', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:EB:DE', 0, 24.5, 'Flower care', 0, 250, 100, '3.1.9', '2019-07-05 22:43:23.976831', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:80:84', 0, 25.1, 'Flower care', 0, 217, 100, '3.2.1', '2019-07-05 22:43:24.014567', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:EB:DE', 0, 24.5, 'Flower care', 0, 8, 100, '3.1.9', '2019-07-05 22:43:42.028918', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:80:84', 0, 25.1, 'Flower care', 0, 0, 100, '3.2.1', '2019-07-05 22:43:42.067098', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:EB:DE', 0, 24.4, 'Flower care', 0, 222, 100, '3.1.9', '2019-07-05 22:44:21.985022', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:80:84', 0, 25.0, 'Flower care', 0, 168, 100, '3.2.1', '2019-07-05 22:44:22.010207', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:EB:DE', 0, 24.3, 'Flower care', 0, 237, 100, '3.1.9', '2019-07-05 22:44:49.059267', NULL);
INSERT INTO public.sensores_mi_flora_historico (mac_addr, humidade, temperatura, nombre, nivel_ph, luz_solar, nivel_bateria, firmware, fecha, zona) VALUES ('C4:7C:8D:6A:80:84', 0, 25.1, 'Flower care', 0, 214, 100, '3.2.1', '2019-07-05 22:44:49.096724', NULL);


--
-- TOC entry 2155 (class 0 OID 16432)
-- Dependencies: 189
-- Data for Name: zona; Type: TABLE DATA; Schema: public; Owner: pi
--

INSERT INTO public.zona (id_zona, canal_gpio, tope_riegos, min_humidade, max_humidade) VALUES ('maceta_2', 21, 5, NULL, NULL);
INSERT INTO public.zona (id_zona, canal_gpio, tope_riegos, min_humidade, max_humidade) VALUES ('maceta_1', 21, 5, 15, 60);


--
-- TOC entry 2025 (class 2606 OID 16395)
-- Name: eventos_rego eventos_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.eventos_rego
    ADD CONSTRAINT eventos_pkey PRIMARY KEY (id);


--
-- TOC entry 2027 (class 2606 OID 16417)
-- Name: sensores_mi_flora pk_sensores_mi_flora; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.sensores_mi_flora
    ADD CONSTRAINT pk_sensores_mi_flora PRIMARY KEY (mac_addr);


--
-- TOC entry 2029 (class 2606 OID 16431)
-- Name: sensores_mi_flora_historico pk_sensores_mi_flora_hist; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.sensores_mi_flora_historico
    ADD CONSTRAINT pk_sensores_mi_flora_hist PRIMARY KEY (mac_addr, fecha);


--
-- TOC entry 2031 (class 2606 OID 16436)
-- Name: zona pk_zona; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.zona
    ADD CONSTRAINT pk_zona PRIMARY KEY (id_zona);


--
-- TOC entry 2023 (class 2606 OID 16390)
-- Name: propiedades pkey_propierties; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.propiedades
    ADD CONSTRAINT pkey_propierties PRIMARY KEY (clave);


--
-- TOC entry 2032 (class 2606 OID 16437)
-- Name: sensores_mi_flora fk_zona_evento; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.sensores_mi_flora
    ADD CONSTRAINT fk_zona_evento FOREIGN KEY (zona) REFERENCES public.zona(id_zona);


--
-- TOC entry 2033 (class 2606 OID 16442)
-- Name: sensores_mi_flora_historico fk_zona_hist; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.sensores_mi_flora_historico
    ADD CONSTRAINT fk_zona_hist FOREIGN KEY (zona) REFERENCES public.zona(id_zona);


--
-- TOC entry 2163 (class 0 OID 0)
-- Dependencies: 7
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2019-07-06 08:41:21 CEST

--
-- PostgreSQL database dump complete
--

