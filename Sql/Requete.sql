-- Active: 1776292121099@@127.0.0.1@1433@model
SELECT session_id, login_name, status
FROM sys.dm_exec_sessions
WHERE database_id = DB_ID('model');
GO

KILL 52;
GO