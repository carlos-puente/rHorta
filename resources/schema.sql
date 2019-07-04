CREATE TABLE public.sensores_mi_flora
(
  mac_addr character varying(50) NOT NULL,
  humidade numeric,
  temperatura numeric,
  nombre character varying(255),
  nivel_ph numeric,
  luz_solar numeric,
  nivel_bateria numeric,
  firmware character varying(10),
  ultima_medicion timestamp without time zone,
  CONSTRAINT pk_sensores_mi_flora PRIMARY KEY (mac_addr)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.sensores_mi_flora
  OWNER TO pi;

CREATE TABLE public.propiedades
(
  clave character varying(50) NOT NULL,
  valor character varying(255),
  CONSTRAINT pkey_propierties PRIMARY KEY (clave)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.propiedades
  OWNER TO pi;
CREATE TABLE public.eventos_rego
(
  id integer NOT NULL,
  inicio timestamp without time zone,
  fin timestamp without time zone,
  zona character varying(50),
  CONSTRAINT eventos_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.eventos_rego
  OWNER TO pi;

INSERT INTO public.propiedades (clave, valor) VALUES ('id_evento', '0');
INSERT INTO public.propiedades (clave, valor) VALUES ('estado_rego', 'INACTIVO');

