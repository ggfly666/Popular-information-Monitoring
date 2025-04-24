from django.contrib.auth.models import User
from ninja import NinjaAPI, Schema
from ninja.errors import HttpError
from django.http import HttpResponse
from django.core.mail import EmailMessage
from typing import List
from .models import Wb, Bd, Bl, CrawlTime, PushTime
import os
import jieba
from wordcloud import WordCloud
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from datetime import datetime
from snownlp import SnowNLP

api = NinjaAPI()

class UserLoginIn(Schema):
    username: str
    password: str

class UserRegisterIn(Schema):
    username: str
    password: str
    email: str
    is_superuser: bool = False

class UserOut(Schema):
    id : int
    username: str
    password: str
    email: str
    is_active: bool
    is_superuser: bool

class UserListOut(Schema):
    id : int
    username: str
    is_superuser: bool
    is_active: bool

class UserUpdateIn(Schema):
    username: str
    updateusername: str = None
    updatepassword: str = None
    updateemail: str = None

class HotListOut(Schema):
    ranking: int
    info: str
    url: str
    hot: str
    uptime: str

class CrawlTimeIn(Schema):
    username: str
    Bdtime: int = 0
    Bltime: int = 0
    Wbtime: int = 0

class CrawlTimeOut(Schema):
    Bdtime: int
    Bltime: int
    Wbtime: int

class PushTimeIn(Schema):
    username: str
    Bdtime: int = 0
    Bltime: int = 0
    Wbtime: int = 0

class PushTimeOut(Schema):
    Bdtime: int
    Bltime: int
    Wbtime: int

@api.post('login')
def login(request, user_in: UserLoginIn):
    user = User.objects.filter(username=user_in.username).first()
    if user is None:
        raise HttpError(400, '登录失败，请检查用户名！')
    if user.is_active is False:
        raise HttpError(400, '用户已被禁用！')
    if user.check_password(user_in.password):
        return {
            'message': '登陆成功！',
            'username': user.username,
            'is_superuser': user.is_superuser
            }
    else:
        raise HttpError(400, '登录失败，请检查密码！')


@api.post('register')
def register(request, user_in: UserRegisterIn):
    if User.objects.filter(username=user_in.username).exists():
        raise HttpError(400, '用户名已创建！')
    else:
        user = User.objects.create_user(
            username=user_in.username,
            password=user_in.password,
            email=user_in.email,
            is_active=True,
            is_superuser=user_in.is_superuser,
        )
        user.save()
        return {'message': '注册成功！'}
    

@api.get('userinfo')
def getuserinfo(request, username: str):
    user = User.objects.filter(username=username).first()
    if user:
        return UserOut(
            id=user.id,
            username=user.username,
            password=user.password,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser
            )
    else:
        raise HttpError(400, '用户不存在！')


@api.post('updateuser')
def updateuser(request, user_in: UserUpdateIn):
    if User.objects.filter(username=user_in.username).exists():    
        if User.objects.filter(username=user_in.updateusername).exists():
            raise HttpError(400, '更新失败，用户名已存在！')
        else:
            user = User.objects.filter(username=user_in.username).first()
            if user_in.updateusername:
                user.username = user_in.updateusername
                user.save()
            elif user_in.updatepassword:
                user.set_password(user_in.updatepassword)
                user.save()
            elif user_in.updateemail:
                user.email = user_in.updateemail
                user.save()
            else:
                raise HttpError(400, '修改失败！')   
        return {'message': '修改成功！'}
    else:
        raise HttpError(400, '用户不存在！')
    

@api.get('userlist',response=List[UserListOut])
def userlist(request, username: str):
    user = User.objects.filter(username=username).first()
    if user.is_superuser:
        users = User.objects.all()
        return users
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.get('activateuser')
def useractivate(request, username: str):
    user = User.objects.filter(username=username).first()
    user.is_active = True
    user.save()
    return {'message': '用户启用成功！'}


@api.get('deactivateuser')
def userdeactivate(request, username: str):
    user = User.objects.filter(username=username).first()
    if user.username == 'admin':
        raise HttpError(400, '该用户无法被禁用！')
    else:
        user.is_active = False
        user.save()
        return {'message': '用户禁用成功！'}


@api.get('deleteuser')
def userdelete(request, username: str):
    user = User.objects.filter(username=username).first()
    if user.username == 'admin':
        raise HttpError(400, '该用户不能被删除！')
    else:
        user.delete()
        return {'message': '用户删除成功！'}


@api.get('resetpassword')
def resetpassword(request, username: str):
    user = User.objects.filter(username=username).first()
    password = '123456'
    user.set_password(password)
    user.save()
    return {'message': '密码已重置！'}


@api.get('systemlog')
def systemlog(request, username: str):
    logpath = os.path.join('./django.log') 
    user = User.objects.filter(username=username).first()
    if user.is_superuser:    
        with open(logpath, 'r') as f:
            return f.read()
    else:
        raise HttpError(400, '用户凭证不正确！')
    

@api.get('desystemlog')
def desystemlog(request, username: str):
    logpath = os.path.join('./django.log')    
    user = User.objects.filter(username=username).first()
    if user.is_superuser:
        with open(logpath, 'w') as f:
            f.write('')
        return {'message': '日志文件已清空！'}
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.get('crawlerlog')
def crawlerlog(request, username: str):
    logpath = os.path.join('../scrapy/scrapy.log')
    user = User.objects.filter(username=username).first()
    if user.is_superuser:
        with open(logpath, 'r') as f:
            return f.read()
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.get('decrawlerlog')
def decrawlerlog(request, username: str):
    logpath = os.path.join('../scrapy/scrapy.log')    
    user = User.objects.filter(username=username).first()
    if user.is_superuser:
        with open(logpath, 'w') as f:
            f.write('')
        return {'message': '日志文件已清空！'}
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.get('crawltime', response=CrawlTimeOut)
def getcrawltime(request, username: str):
    user = User.objects.filter(username=username).first()
    if user.is_superuser:
        crawltimes = CrawlTime.objects.order_by('id').first()
        if crawltimes:
            return crawltimes  
        else:
            raise HttpError(400, '未找到爬取时间配置！')
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.get('pushtime', response=PushTimeOut)
def getpushtime(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        pushtimes = PushTime.objects.order_by('id').first()
        if pushtimes:
            return pushtimes  
        else:
            raise HttpError(400, '未找到推送时间配置！')
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.post('updatecrawltime')
def updatecrawltime(request, crawltime_in: CrawlTimeIn):
    user = User.objects.filter(username=crawltime_in.username).first()
    if user.is_superuser:
        crawltimes = CrawlTime.objects.order_by('id').first()
        if crawltimes:
            if crawltime_in.Bdtime:
                crawltimes.Bdtime = crawltime_in.Bdtime
                crawltimes.save()
            if crawltime_in.Bltime:
                crawltimes.Bltime = crawltime_in.Bltime
                crawltimes.save()
            if crawltime_in.Wbtime:
                crawltimes.Wbtime = crawltime_in.Wbtime
                crawltimes.save()   
        return {'message': '时间修改成功！'}
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.post('updatepushtime')
def updatepushtime(request, pushtime_in: PushTimeIn):
    user = User.objects.filter(username=pushtime_in.username).first()
    if user is not None:
        pushtimes = PushTime.objects.order_by('id').first()
        if pushtimes:
            if pushtime_in.Bdtime:
                pushtimes.Bdtime = pushtime_in.Bdtime
                pushtimes.save()
            if pushtime_in.Bltime:
                pushtimes.Bltime = pushtime_in.Bltime
                pushtimes.save()
            if pushtime_in.Wbtime:
                pushtimes.Wbtime = pushtime_in.Wbtime
                pushtimes.save()
        return {'message': '时间修改成功！'}
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.get('wbhotinfo', response=List[HotListOut])
def wbhotinfo(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        wbs = Wb.objects.order_by('-uptime')[:30]
        wbs_sorted = sorted(wbs, key=lambda x: x.ranking)
        formatted_wbs = [
            {
                'ranking': wb.ranking,
                'info': wb.info,
                'url': wb.url,
                'hot': wb.hot,
                'uptime': wb.uptime.strftime('%Y-%m-%d %H:%M:%S')
            }
            for wb in wbs_sorted
        ]
        return formatted_wbs
    else:
        raise HttpError(400, '用户凭证不正确！')
    

@api.get('wbhotwordcloud')
def wbhotwordcloud(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        wbs = Wb.objects.order_by('-uptime')[:90] 
        if not wbs:
            raise {'word_freq': {}}
        else:
            text_content = ' '.join([wb.info for wb in wbs])
            words = jieba.lcut(text_content)
            stopwords = {'的', '是', '了', '在', '等'}  
            filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
            word_freq = {}
            for word in filtered_words:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
            return {'word_freq': word_freq}
    else:
        raise HttpError(400, '用户凭证不正确！')
        

@api.get('wblinechart')
def wblinechart(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        today = datetime.today()
        month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        wbs = Wb.objects.filter(uptime__gte=month).filter(ranking__in=[1, 2, 3]).order_by('ranking', 'uptime')
        formatted_wbs = [
            {
                'ranking': wb.ranking,
                'info': wb.info,
                'url': wb.url,
                'hot': wb.hot,
                'uptime': wb.uptime.strftime('%Y-%m-%d %H:%M:%S')
            }
            for wb in wbs
        ]
        return formatted_wbs
    else:
        raise HttpError(400, '用户凭证不正确！')

@api.get('wbhotsentiment')
def wbhotsentiment(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        wbs = Wb.objects.order_by('-uptime')[:30]
        texts = [wb.info for wb in wbs]
        sentiments = [SnowNLP(text).sentiments for text in texts]
        positive = sum(1 for s in sentiments if s > 0.6)
        neutral = sum(1 for s in sentiments if 0.4 <= s <= 0.6)
        negative = sum(1 for s in sentiments if s < 0.4)  
        font_path = './font/simhei.ttf' 
        chinese_font = FontProperties(fname=font_path, size=10)  
        labels = ['正面', '中性', '负面']
        sizes = [positive, neutral, negative]
        total = sum(sizes)
        colors = ['#99ff99', '#ffcc99', '#ff6666']
        labeled_sizes = [f'{label}\n({size})' for label, size in zip(labels, sizes)]
        fig, ax = plt.subplots(figsize=(4, 4))  
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labeled_sizes,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontproperties': chinese_font, 'size': 8}, 
            wedgeprops={'edgecolor': 'white', 'width': 0.3}  
        )
        plt.setp(autotexts, size=8, weight="bold", fontproperties=chinese_font)  
        plt.setp(texts, size=8, fontproperties=chinese_font)  
        ax.axis('equal')
        plt.title(f'微博热门情感分析\n(共{total}条)', 
                 fontproperties=chinese_font, 
                 pad=10, 
                 fontsize=10)  
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, 
                   format='png', 
                   dpi=150,  
                   bbox_inches='tight')
        plt.close(fig)  
        buffer.seek(0)
        return HttpResponse(buffer.getvalue(), content_type="image/png")
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.get('wbhotsentiment/push')
def wbhotsentiment_push(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        wbs = Wb.objects.order_by('-uptime')[:30]
        texts = [wb.info for wb in wbs]
        sentiments = [SnowNLP(text).sentiments for text in texts]
        positive = sum(1 for s in sentiments if s > 0.6)
        neutral = sum(1 for s in sentiments if 0.4 <= s <= 0.6)
        negative = sum(1 for s in sentiments if s < 0.4)  
        font_path = './font/simhei.ttf' 
        chinese_font = FontProperties(fname=font_path, size=10)  
        labels = ['正面', '中性', '负面']
        sizes = [positive, neutral, negative]
        total = sum(sizes)
        colors = ['#99ff99', '#ffcc99', '#ff6666']
        labeled_sizes = [f'{label}\n({size})' for label, size in zip(labels, sizes)]
        fig, ax = plt.subplots(figsize=(4, 4))  
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labeled_sizes,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontproperties': chinese_font, 'size': 8}, 
            wedgeprops={'edgecolor': 'white', 'width': 0.3}  
        )
        plt.setp(autotexts, size=8, weight="bold", fontproperties=chinese_font)  
        plt.setp(texts, size=8, fontproperties=chinese_font)  
        ax.axis('equal')
        plt.title(f'微博热门情感分析\n(共{total}条)', 
            fontproperties=chinese_font, 
            pad=10, 
            fontsize=10)  
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, 
            format='png', 
            dpi=150,  
            bbox_inches='tight')
        plt.close(fig)  
        buffer.seek(0)
        if (negative + neutral) / total >= 0.7:
            try:
                email = EmailMessage(
                    subject='微博热门情感分析（高风险）',
                    body='微博热门存在的中性与负面情感占比超过70%，存在高风险，请查收附件——微博热门情感分析图。',
                    from_email='13720105121@163.com',  
                    to=[user.email]
                )
                email.attach('附件.png', buffer.read(), 'image/png')
                email.send(fail_silently=False)
            except Exception as e:
                raise HttpError(500, f'邮件发送失败：{str(e)}')
            return {'message': '邮件发送成功！'}
        elif (negative + neutral) / total >= 0.5:
            try:
                email = EmailMessage(
                    subject='微博热门情感分析（中风险）',
                    body='微博热门存在的中性与负面情感占比超过50%，存在中风险，请查收附件——微博热门情感分析图。',
                    from_email='13720105121@163.com',  
                    to=[user.email]
                )
                email.attach('附件.png', buffer.read(), 'image/png')
                email.send(fail_silently=False)
            except Exception as e:
                raise HttpError(500, f'邮件发送失败：{str(e)}')
            return {'message': '邮件发送成功！'}
        elif (negative + neutral) / total >= 0.3:
            try:
                email = EmailMessage(
                    subject='微博热门情感分析（低风险）',
                    body='微博热门存在的中性与负面情感占比超于30%，存在低风险，请查收附件——微博热门情感分析图。',
                    from_email='13720105121@163.com',  
                    to=[user.email]
                )
                email.attach('附件.png', buffer.read(), 'image/png')
                email.send(fail_silently=False)
            except Exception as e:
                raise HttpError(500, f'邮件发送失败：{str(e)}')
            return {'message': '邮件发送成功！'}
        else:
            return {'message': '未检测到风险！'}
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.get('bdhotinfo', response=List[HotListOut])
def bdhotinfo(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        bds = Bd.objects.order_by('-uptime')[:30]
        bds_sorted = sorted(bds, key=lambda x: x.ranking)
        formatted_bds = [
            {
                'ranking': bd.ranking,
                'info': bd.info,
                'url': bd.url,
                'hot': bd.hot,
                'uptime': bd.uptime.strftime('%Y-%m-%d %H:%M:%S')
            }
            for bd in bds_sorted
        ]
        return formatted_bds
    else:
        raise HttpError(400, '用户凭证不正确！')
    

@api.get('bdhotwordcloud')
def bdhotwordcloud(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        bds = Bd.objects.order_by('-uptime')[:90]   
        text_content = ' '.join([bd.info for bd in bds])
        words = jieba.lcut(text_content)
        stopwords = {'的', '是', '了', '在', '等'}
        filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
        word_freq = {}
        for word in filtered_words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        bd = WordCloud(
            font_path='./font/simhei.ttf',  
            background_color='white',
            width=800,
            height=400, 
        ).generate_from_frequencies(word_freq)
        img = BytesIO()
        plt.imshow(bd, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.savefig(img, format='PNG', transparent=True, bbox_inches='tight', pad_inches=0)
        plt.close()
        img.seek(0)
        return HttpResponse(img.getvalue(), content_type='image/png')
    else:
        raise HttpError(400, '用户凭证不正确！')         


@api.get('bdhotsentiment')
def bdhotsentiment(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        bds = Bd.objects.order_by('-uptime')[:30]
        texts = [bd.info for bd in bds]
        sentiments = [SnowNLP(text).sentiments for text in texts]
        positive = sum(1 for s in sentiments if s > 0.6)
        neutral = sum(1 for s in sentiments if 0.4 <= s <= 0.6)
        negative = sum(1 for s in sentiments if s < 0.4)  
        font_path = './font/simhei.ttf' 
        chinese_font = FontProperties(fname=font_path, size=10)  
        labels = ['正面', '中性', '负面']
        sizes = [positive, neutral, negative]
        total = sum(sizes)
        colors = ['#99ff99', '#ffcc99', '#ff6666']
        labeled_sizes = [f'{label}\n({size})' for label, size in zip(labels, sizes)]
        fig, ax = plt.subplots(figsize=(4, 4))  
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labeled_sizes,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontproperties': chinese_font, 'size': 8}, 
            wedgeprops={'edgecolor': 'white', 'width': 0.3}  
        )
        plt.setp(autotexts, size=8, weight="bold", fontproperties=chinese_font)  
        plt.setp(texts, size=8, fontproperties=chinese_font)  
        ax.axis('equal')
        plt.title(f'百度热门情感分析\n(共{total}条)', 
                 fontproperties=chinese_font, 
                 pad=10, 
                 fontsize=10)  
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, 
                   format='png', 
                   dpi=150,  
                   bbox_inches='tight')
        plt.close(fig)  
        buffer.seek(0)
        return HttpResponse(buffer.getvalue(), content_type="image/png")
    else:
        raise HttpError(400, '用户凭证不正确！')
    

@api.get('bdhotsentiment/push')
def bdhotsentiment_push(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        bds = Bd.objects.order_by('-uptime')[:30]
        texts = [bd.info for bd in bds]
        sentiments = [SnowNLP(text).sentiments for text in texts]
        positive = sum(1 for s in sentiments if s > 0.6)
        neutral = sum(1 for s in sentiments if 0.4 <= s <= 0.6)
        negative = sum(1 for s in sentiments if s < 0.4)  
        font_path = './font/simhei.ttf' 
        chinese_font = FontProperties(fname=font_path, size=10)  
        labels = ['正面', '中性', '负面']
        sizes = [positive, neutral, negative]
        total = sum(sizes)
        colors = ['#99ff99', '#ffcc99', '#ff6666']
        labeled_sizes = [f'{label}\n({size})' for label, size in zip(labels, sizes)]
        fig, ax = plt.subplots(figsize=(4, 4))  
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labeled_sizes,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontproperties': chinese_font, 'size': 8}, 
            wedgeprops={'edgecolor': 'white', 'width': 0.3}  
        )
        plt.setp(autotexts, size=8, weight="bold", fontproperties=chinese_font)  
        plt.setp(texts, size=8, fontproperties=chinese_font)  
        ax.axis('equal')
        plt.title(f'百度热门情感分析\n(共{total}条)', 
                 fontproperties=chinese_font, 
                 pad=10, 
                 fontsize=10)  
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, 
                   format='png', 
                   dpi=150,  
                   bbox_inches='tight')
        plt.close(fig)  
        buffer.seek(0)
        if (negative + neutral) / total >= 0.7:
            try:
                email = EmailMessage(
                    subject='百度热门情感分析（高风险）',
                    body='百度热门存在的中性与负面情感占比超过70%，存在高风险，请查收附件——百度热门情感分析图。',
                    from_email='13720105121@163.com',  
                    to=[user.email]
                )
                email.attach('附件.png', buffer.read(), 'image/png')
                email.send(fail_silently=False)
            except Exception as e:
                raise HttpError(500, f'邮件发送失败：{str(e)}')
            return {'message': '邮件发送成功！'}
        elif (negative + neutral) / total >= 0.5:
            try:
                email = EmailMessage(
                    subject='百度热门情感分析（中风险）',
                    body='百度热门存在的中性与负面情感占比超过50%，存在中风险，请查收附件——百度热门情感分析图。',
                    from_email='13720105121@163.com',  
                    to=[user.email]
                )
                email.attach('附件.png', buffer.read(), 'image/png')
                email.send(fail_silently=False)
            except Exception as e:
                raise HttpError(500, f'邮件发送失败：{str(e)}')
            return {'message': '邮件发送成功！'}
        elif (negative + neutral) / total >= 0.3:
            try:
                email = EmailMessage(
                    subject='百度热门情感分析（低风险）',
                    body='百度热门存在的中性与负面情感占比超过30%，存在低风险，请查收附件——百度热门情感分析图。',
                    from_email='13720105121@163.com',  
                    to=[user.email]
                )
                email.attach('附件.png', buffer.read(), 'image/png')
                email.send(fail_silently=False)
            except Exception as e:
                raise HttpError(500, f'邮件发送失败：{str(e)}')
            return {'message': '邮件发送成功！'}
        else:
            return {'message': '未检测到风险！'}
    else:
        raise HttpError(400, '用户凭证不正确！')


@api.get('blhotinfo', response=List[HotListOut])
def blhotinfo(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        bls = Bl.objects.order_by('-uptime')[:30]
        bls_sorted = sorted(bls, key=lambda x: x.ranking)
        formatted_bls = [
            {
                'ranking': bl.ranking,
                'info': bl.info,
                'url': bl.url,
                'hot': bl.hot,
               'uptime': bl.uptime.strftime('%Y-%m-%d %H:%M:%S')
            }
            for bl in bls_sorted
        ]
        return formatted_bls
    else:
        raise HttpError(400, '用户凭证不正确！')
    

@api.get('blhotwordcloud')
def blhotwordcloud(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        bls = Bl.objects.order_by('-uptime')[:90]
        text_content = ' '.join([bl.info for bl in bls])
        words = jieba.lcut(text_content)
        stopwords = {'的', '是', '了', '在', '等'}
        filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
        word_freq = {}
        for word in filtered_words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        bl = WordCloud(
            font_path='./font/simhei.ttf',  
            background_color='white',
            width=800,
            height=400
        ).generate_from_frequencies(word_freq)
        img = BytesIO()
        plt.imshow(bl, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.savefig(img, format='PNG', transparent=True, bbox_inches='tight', pad_inches=0)
        plt.close()
        img.seek(0)
        return HttpResponse(img.getvalue(), content_type='image/png')
    else:
        raise HttpError(400, '用户凭证不正确！')
    

@api.get('blhotsentiment')
def blhotsentiment(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        bls = Bl.objects.order_by('-uptime')[:30]
        texts = [bl.info for bl in bls]
        sentiments = [SnowNLP(text).sentiments for text in texts]
        positive = sum(1 for s in sentiments if s > 0.6)
        neutral = sum(1 for s in sentiments if 0.4 <= s <= 0.6)
        negative = sum(1 for s in sentiments if s < 0.4)  
        font_path = './font/simhei.ttf' 
        chinese_font = FontProperties(fname=font_path, size=10)  
        labels = ['正面', '中性', '负面']
        sizes = [positive, neutral, negative]
        total = sum(sizes)
        colors = ['#99ff99', '#ffcc99', '#ff6666']
        labeled_sizes = [f'{label}\n({size})' for label, size in zip(labels, sizes)]
        fig, ax = plt.subplots(figsize=(4, 4))  
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labeled_sizes,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontproperties': chinese_font, 'size': 8}, 
            wedgeprops={'edgecolor': 'white', 'width': 0.3}  
        )
        plt.setp(autotexts, size=8, weight="bold", fontproperties=chinese_font)  
        plt.setp(texts, size=8, fontproperties=chinese_font)  
        ax.axis('equal')
        plt.title(f'B站热门情感分析\n(共{total}条)', 
                 fontproperties=chinese_font, 
                 pad=10, 
                 fontsize=10)  
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, 
                   format='png', 
                   dpi=150,  
                   bbox_inches='tight')
        plt.close(fig)  
        buffer.seek(0)
        return HttpResponse(buffer.getvalue(), content_type="image/png")
    else:
        raise HttpError(400, '用户凭证不正确！')
    

@api.get('blhotsentiment/push')
def blhotsentiment_push(request, username: str):
    user = User.objects.filter(username=username).first()
    if user is not None:
        bls = Bl.objects.order_by('-uptime')[:30]
        texts = [bl.info for bl in bls]
        sentiments = [SnowNLP(text).sentiments for text in texts]
        positive = sum(1 for s in sentiments if s > 0.6)
        neutral = sum(1 for s in sentiments if 0.4 <= s <= 0.6)
        negative = sum(1 for s in sentiments if s < 0.4)  
        font_path = './font/simhei.ttf' 
        chinese_font = FontProperties(fname=font_path, size=10)  
        labels = ['正面', '中性', '负面']
        sizes = [positive, neutral, negative]
        total = sum(sizes)
        colors = ['#99ff99', '#ffcc99', '#ff6666']
        labeled_sizes = [f'{label}\n({size})' for label, size in zip(labels, sizes)]
        fig, ax = plt.subplots(figsize=(4, 4))  
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labeled_sizes,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontproperties': chinese_font, 'size': 8}, 
            wedgeprops={'edgecolor': 'white', 'width': 0.3}  
        )
        plt.setp(autotexts, size=8, weight="bold", fontproperties=chinese_font)  
        plt.setp(texts, size=8, fontproperties=chinese_font)  
        ax.axis('equal')
        plt.title(f'B站热门情感分析\n(共{total}条)', 
                 fontproperties=chinese_font, 
                 pad=10, 
                 fontsize=10)  
        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, 
                   format='png', 
                   dpi=150,  
                   bbox_inches='tight')
        plt.close(fig)  
        buffer.seek(0)
        if (negative + neutral) / total >= 0.7:
            try:
                email = EmailMessage(
                    subject='B站热门情感分析（高风险）',
                    body='B站热门存在的中性与负面情感占比超过70%，存在高风险，请查收附件——B站热门情感分析图。',
                    from_email='13720105121@163.com',  
                    to=[user.email]
                )
                email.attach('附件.png', buffer.read(), 'image/png')
                email.send(fail_silently=False)
            except Exception as e:
                raise HttpError(500, f'邮件发送失败：{str(e)}')
            return {'message': '邮件发送成功！'}
        elif (negative + neutral) / total >= 0.5:
            try:
                email = EmailMessage(
                    subject='B站热门情感分析（中风险）',
                    body='B站热门存在的中性与负面情感占比超过50%，存在中风险，请查收附件——B站热门情感分析图。',
                    from_email='13720105121@163.com',  
                    to=[user.email]
                )
                email.attach('附件.png', buffer.read(), 'image/png')
                email.send(fail_silently=False)
            except Exception as e:
                raise HttpError(500, f'邮件发送失败：{str(e)}')
            return {'message': '邮件发送成功！'}
        elif (negative + neutral) / total >= 0.3:
            try:
                email = EmailMessage(
                    subject='B站热门情感分析（低风险）',
                    body='B站热门存在的中性与负面情感占比超过30%，存在低风险，请查收附件——B站热门情感分析图。',
                    from_email='13720105121@163.com',  
                    to=[user.email]
                )
                email.attach('附件.png', buffer.read(), 'image/png')
                email.send(fail_silently=False)
            except Exception as e:
                raise HttpError(500, f'邮件发送失败：{str(e)}')
            return {'message': '邮件发送成功！'}
        else:
            return {'message': '未检测到风险！！'}
    else:
        raise HttpError(400, '用户凭证不正确！')