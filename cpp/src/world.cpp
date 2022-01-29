/* Copyright (c) 2022 Pixel Flux
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#include "world.hpp"

using namespace pyflecs;

world::world() : 
    mpRaw(ecs_init())
{

}

world::~world()
{
    ecs_fini(mpRaw);
}

pyflecs::entity world::entity()
{
    return pyflecs::entity(mpRaw, ecs_new_id(mpRaw));
}

pyflecs::entity world::entity(std::string name)
{
    ecs_entity_desc_t desc{};
    desc.name = name.c_str();
    ecs_entity_init(mpRaw, &desc);
    return pyflecs::entity(mpRaw, ecs_entity_init(mpRaw, &desc));
}

pyflecs::entity world::lookup(std::string name)
{
    ecs_lookup(mpRaw, name.c_str());
    return pyflecs::entity(mpRaw, ecs_lookup(mpRaw, name.c_str()));
}

pyflecs::component world::component(std::string name, size_t size, 
    size_t alignment)
{
    return pyflecs::component(mpRaw, name, size, alignment);
}
