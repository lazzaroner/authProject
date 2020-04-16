# __author__:"xgh"
# date: 2020/3/7
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


def table_filter(request, admin_class):
    """进行条件过滤，并返回过滤后的数据"""
    filter_conditions = []
    for k, v in request.GET.items():
        if v:
            if k == "page":
                continue
            filter_conditions.append((k, v))
    con = Q()
    q1 = Q()
    q1.connector = 'OR'
    # 针对search_fields进行Q操作
    for item in filter_conditions:
        if item[0] == 'q':
            if admin_class.search_fields:
                for filter_field in admin_class.search_fields:
                    q1.children.append(('%s__icontains' % filter_field, item[1]))
    con.add(q1, 'AND')

    # 针对list_filter进行Q操作
    filter_dict = {}
    for item in filter_conditions:
        # 移除q条件
        if item[0] == 'q':
            continue
        # 这里对k_v=v对形式进行解析，并将一个key对应的值放到一个字典里面，不同的key使用and进行连接
        key = item[0].split('_')[0]
        # filter_dict[key] = []
        if filter_dict.get(key):
            filter_dict[key].append(item[1])
        else:
            filter_dict[key] = [item[1]]

    q2 = Q()
    if filter_dict:
        for k, v in filter_dict.items():
            q3 = Q()
            q3.connector = 'OR'
            for sub_k in v:
                q3.children.append((k, sub_k))
            q2.add(q3, 'AND')

    con.add(q2, 'AND')

    return admin_class.model.objects.filter(con).order_by('id'), filter_conditions


def split_page(object_list, page_num=None, per_page=8):
    paginator = Paginator(object_list, per_page)
    # 取出当前需要展示的页码, 默认为1
    # 根据页码从分页器中取出对应页的数据
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger as e:
        # 不是整数返回第一页数据
        page = paginator.page('1')
        page_num = 1
    except EmptyPage as e:
        # 当参数页码大于或小于页码范围时,会触发该异常
        print('EmptyPage:{}'.format(e))
        if int(page_num) > paginator.num_pages:
            # 大于 获取最后一页数据返回
            page = paginator.page(paginator.num_pages)
        else:
            # 小于 获取第一页
            page = paginator.page(1)

    # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
    page_num = int(page_num)
    if page_num < 6:
        if paginator.num_pages <= 11:
            dis_range = range(1, paginator.num_pages + 1)
        else:
            dis_range = range(1, 12)
    elif (page_num >= 6) and (page_num <= paginator.num_pages - 5):
        dis_range = range(page_num - 5, page_num + 6)
    elif (page_num >= 6) and (paginator.num_pages - page_num < 5):
        dis_range = range(paginator.num_pages-10, paginator.num_pages + 1)
    else:
        dis_range = range(paginator.num_pages - 9, paginator.num_pages + 1)

    page_previous = page_num - 1
    page_next = page_num + 1
    if page_previous < 1 :
        page_previous = 1
    if page_next > paginator.num_pages:
        page_next = paginator.num_pages

    data = {'page': page, 'paginator': paginator, 'dis_range': dis_range, 'page_num': page_num,
            "page_previous": page_previous, "page_next": page_next, 'record_count': paginator.count}

    return data
