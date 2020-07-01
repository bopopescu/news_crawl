create table image_urls
(
    id        bigint auto_increment
        primary key,
    url       varchar(255) null,
    image_url varchar(255) null
);

create table industries
(
    code varchar(20)  not null
        primary key,
    name varchar(255) null
);

create table keywords
(
    id   int auto_increment
        primary key,
    name varchar(100) null
);

create table posts
(
    id               bigint auto_increment
        primary key,
    title            varchar(255)  null,
    summary          varchar(5000) null,
    published        datetime      null,
    created          datetime      null,
    url              varchar(255)  null,
    image_url        varchar(255)  null,
    tokenize_content text          null
);

create table post_ratings
(
    id      bigint auto_increment
        primary key,
    postId  bigint                   null,
    rate    int                      null,
    source  varchar(45) charset utf8 null,
    created datetime                 null,
    constraint post_ratings_ibfk_1
        foreign key (postId) references posts (id)
);

create index postId
    on post_ratings (postId);

create table post_tags
(
    id        bigint auto_increment
        primary key,
    postId    bigint            null,
    content   text charset utf8 null,
    symbol    varchar(20)       null,
    sentiment varchar(3)        null,
    constraint post_tags_ibfk_1
        foreign key (postId) references posts (id)
);

create index postId
    on post_tags (postId);

create table stock_keywords
(
    symbol    varchar(255) null,
    keywordId int          null
);

create table stocks
(
    symbol       varchar(20)  not null
        primary key,
    companyName  varchar(500) null,
    industryCode varchar(20)  null
);

