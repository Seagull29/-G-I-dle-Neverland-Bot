create table if not exists exp (
    UserID integer primary key,
    XP integer default 0,
    Levels integer default 0,
    XPLock text default current_timestamp
);

create table if not exists guilds (
    GuildID integer primary key,
    Prefix text default "!"
);

