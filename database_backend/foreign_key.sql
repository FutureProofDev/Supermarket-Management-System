alter table employee
    add constraint employee_user_id_fk_auth_user_id
    foreign key (user_id) references auth_user(id);