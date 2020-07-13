create table industries
(
    code varchar(20)               not null
        primary key,
    name varchar(255) charset utf8 null
);

create table keywords
(
    id   int auto_increment
        primary key,
    name varchar(255) charset utf8 null
);

create table posts
(
    id               bigint auto_increment
        primary key,
    title            varchar(500) charset utf8 null,
    summary          text charset utf8         null,
    published        datetime                  null,
    created          datetime                  null,
    url              varchar(255)              null,
    image_url        varchar(255)              null,
    tokenize_content longtext charset utf8     null,
    is_ready         bit                       null
);

create table post_ratings
(
    id      bigint auto_increment
        primary key,
    postId  bigint                    null,
    rate    int                       null,
    source  varchar(100) charset utf8 null,
    created datetime                  null,
    constraint post_ratings_ibfk_1
        foreign key (postId) references posts (id)
);

create index postId
    on post_ratings (postId);

create table stocks
(
    symbol       varchar(20)               not null
        primary key,
    companyName  varchar(255) charset utf8 null,
    industryCode varchar(20)               null,
    constraint stocks_ibfk_1
        foreign key (industryCode) references industries (code)
);

create table post_tags
(
    id        bigint auto_increment
        primary key,
    postId    bigint                null,
    symbol    varchar(20)           null,
    content   longtext charset utf8 null,
    sentiment varchar(3)            null,
    constraint post_tags_ibfk_1
        foreign key (postId) references posts (id),
    constraint post_tags_ibfk_2
        foreign key (symbol) references stocks (symbol)
);

create index postId
    on post_tags (postId);

create index symbol
    on post_tags (symbol);

create table stock_keywords
(
    id        int auto_increment
        primary key,
    symbol    varchar(20) null,
    keywordId int         null,
    constraint stock_keywords_ibfk_1
        foreign key (symbol) references stocks (symbol),
    constraint stock_keywords_ibfk_2
        foreign key (keywordId) references keywords (id)
);

create index keywordId
    on stock_keywords (keywordId);

create index symbol
    on stock_keywords (symbol);

create index industryCode
    on stocks (industryCode);

