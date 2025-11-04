# ComfyUI Tips

## Best Samplers 

And Schedulers.

### For SRPO

Samplers like Euler, DPM++ 2M Karras, and DPM2 & Karras work well with the SRPO model. For schedulers, Euler and Simple are common choices, though Karras is also popular, especially for DPM++ samplers. Experimentation is key, as the best combination can depend on the specific SRPO model version and the desired outcome. 

**Popular sampler/scheduler combinations**  
- Euler/Simple: A fast combination that can produce good results quickly, with "Simple" often paired with "Euler" in tests.  
- DPM++ 2M Karras: A popular choice that can be effective for pulling out more detail compared to some other samplers.  
- DPM2 a Karras: This sampler, often paired with the Karras scheduler, is another strong contender for detailed results.  

Other samplers to try
DDIM
Heun
LMS
DEIS
Dpm fast 

<hr style="height:12px;border-width:0;color:blue;background-color:blue">

[Back to the Main Page](../index.md)


Note to self: **Quick Links**

[b25]: ../blogs/Blog0925.md
