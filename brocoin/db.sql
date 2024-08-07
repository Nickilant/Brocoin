
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

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.referals_score (
    username character varying,
    score integer
);


ALTER TABLE public.referals_score OWNER TO postgres;


CREATE SEQUENCE public.task_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_id_seq OWNER TO postgres;


CREATE TABLE public.tasks (
    id integer DEFAULT nextval('public.task_id_seq'::regclass) NOT NULL,
    description text NOT NULL,
    points integer NOT NULL,
    image character(1),
    links character varying(255)
);


ALTER TABLE public.tasks OWNER TO postgres;


CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO postgres;


ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;


CREATE TABLE public.user_tasks (
    id integer DEFAULT nextval('public.users_id_seq'::regclass) NOT NULL,
    user_id uuid,
    task_id integer,
    image character varying(255)
);


ALTER TABLE public.user_tasks OWNER TO postgres;


CREATE SEQUENCE public.user_tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_tasks_id_seq OWNER TO postgres;


ALTER SEQUENCE public.user_tasks_id_seq OWNED BY public.user_tasks.id;


CREATE TABLE public.users (
    sid uuid NOT NULL,
    username character varying(255) NOT NULL,
    score integer,
    last_tap timestamp without time zone,
    refs json,
    premium boolean,
    ref_code character varying(255),
    quests json,
    boost date,
    last_score integer,
    energy integer DEFAULT 1000 NOT NULL,
    tickets integer DEFAULT 0
);


ALTER TABLE public.users OWNER TO postgres;


ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.user_tasks
    ADD CONSTRAINT user_tasks_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (sid);


ALTER TABLE ONLY public.user_tasks
    ADD CONSTRAINT user_tasks_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


ALTER TABLE ONLY public.user_tasks
    ADD CONSTRAINT user_tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(sid);

