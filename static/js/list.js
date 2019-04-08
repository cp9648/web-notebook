/**
 * 判断元素是否含有制定的class样式
 */
function has_class(elem, class_name) {
    return elem.className.split(' ').indexOf(class_name) > -1;
}
/**
 * 获取元素属性
 */
function get_attr(elem, attr_name) {
    return elem.getAttribute(attr_name);
}
/**
 * 切换class样式
 */
function toggle_class(elem, class_name) {
    // 有class样式就去掉
    var new_class_name = elem.className;
    if(has_class(elem, class_name)) {
        new_class_name = new_class_name.replace(class_name, ' ');
    }
    else {
        // 否则就添加
        new_class_name = new_class_name + ' ' + class_name;
    }
    // 去掉多余的空格
    elem.className = new_class_name.replace(/\s{2,}/g, ' ').trim();
}
/**
 * 添加class样式
 */
function add_class(elem, class_name) {
    // 如果没有class样式，就切换（添加）
    if(!has_class(elem, class_name)) {
        toggle_class(elem, class_name);
    }
}
/**
 * 移除class样式
 */
function remove_class(elem, class_name) {
    // 如果有class样式，就切换（移除）
    if(has_class(elem, class_name)) {
        toggle_class(elem, class_name);
    }
}
/**
 * 事件绑定封装
 */
function bind_event(elem, event_name, func) {
    if(elem.addEventListener) {
        elem.addEventListener(event_name, func, false);
    }
    else {
        elem.attachEvent('on' + event_name, func);
    }
}
// /////////////////////////=抢镜头-的-分割线=/////////////////////////////////
var e_tags;

/**
 * 收集tags-id
 */
function collect_tags_id() {
    var e_hid_tags = document.querySelector('[name="hid-tags"]');
    var hid_value = '';
    // '全部'
    var tag_all = e_tags.querySelector('[data-id="0"]');
    // 如果全部选中了
    if(has_class(tag_all, 'choose')) {
        hid_value = '';
    }
    else {
        var data_ids = [];
        // 得到所有选中了的元素
        var tags_choose = e_tags.querySelectorAll('.choose');
        for (var i = 0; i < tags_choose.length; i++) {
            var data_id = get_attr(tags_choose[i], 'data-id');
            data_ids.push(data_id);
        }
        hid_value = data_ids.join(',');
    }
    e_hid_tags.value = hid_value;
}
/**
 * 标签click事件处理函数
 */
function tag_click(event) {
    event = event || window.event;
    // 获取点击的元素
    var e_this = event.srcElement || event.target;
    // 根据是否有'tag-itme' class样式，判断是否是点击了标签
    if(has_class(e_this, 'tag-itme')) {
        // 获取'data-id'属性
        var data_id = get_attr(e_this, 'data-id');
        // 判断是否是选中了当前标签(没有选中时，点击后选中)
        var is_select = !has_class(e_this, 'choose');
        // 如果 data-id 为0，说明点击的是'全部'，则取消其他全部的标签的选中
        // '全部'
        var tag_all = e_tags.querySelector('[data-id="0"]');
        if(is_select) {
            var choose_count = e_tags.querySelectorAll('.choose').length,
                tags_count = e_tags.querySelectorAll('.tag-itme').length;
            var click_all = data_id == '0', // 选中'全选'
                all_selected = choose_count == tags_count - 2; // 全部选中
            if(click_all || all_selected) {
                // 得到所有标签元素
                var tags_list = e_tags.querySelectorAll('.tag-itme');
                // 遍历每一个元素，将class样式移除
                for (var i = 0; i < tags_list.length; i++) {
                    remove_class(tags_list[i], 'choose');
                }
                add_class(tag_all, 'choose');
            }
            else {
                if(has_class(tag_all, 'choose')) {
                    toggle_class(tag_all, 'choose');
                }
                toggle_class(e_this, 'choose');
            }
        }
        else {
            if(data_id != '0') {
                toggle_class(e_this, 'choose');
            }
        }
        collect_tags_id();
    }
}
/**
 * windows加载事件绑定
 */
window.onload = function() {
    e_tags = document.querySelector('.tags-wrapper');
    bind_event(e_tags, 'click', tag_click);
    collect_tags_id();
};